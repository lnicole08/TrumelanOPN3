 #defines function to convert .idx files to .csv files
def IndexToCSV(file,output=None, model=None, fps=10,video=1, unique_adj=False):
    """
    A function to convert the whole index file (excluding the header) to a csv

    Parameters
    ----------
    file : Str
        Input .idx file location
    output : Str
        Output .csv file location  
    model : pkl model
        The model used to create the state classifier. If not supplied,
        the basic thresholding will be used (1mm/sec=locomotive, <1mm/sec = Stationary,
        >10px Activity Level = Stationary Active, <10px Activity Level = Stationary Static)
    fps : int (default 10).
        The fps of the recording.
    video : int (0 or 1)
        To say if you had created movr files when doing the experiment. 
        Default is yes (1). If you hadnt, use (0)
    Returns
    -------
    CSV if no output supplied.
    
    Outputs
    -------
    CSV
    """
    
    import struct
    import pandas as pd
    
    
    input_file_name = (file)
    input_file = open(input_file_name, 'rb')

    input_file.read(1)
    data1=input_file.read(4)
    metrics_list_array_size=struct.unpack(">I", data1)
    input_file.read(2*metrics_list_array_size[0])
    data3=input_file.read(4)
    record_size=struct.unpack(">i",data3)

    if video==1:    
        xx=0  
        while (byte := input_file.read(1)): 
            xx=xx+1#The while is to skip past the next few bytes until it finds the .movr bytes
            if b'.' in byte:
                byte = input_file.read(4)
                xx=xx+4
                if byte==b'movr':
                    break
                else:
                    continue
            else:
                continue
    elif video==0:
        xx=0  
        while (byte := input_file.read(1)): 
            xx=xx+1#The while is to skip past the next few bytes until it finds the .movr bytes
            if b'V' in byte:
                byte = input_file.read(3)
                xx=xx+3
                if byte==b'OID':
                    break
                else:
                    continue
            else:
                continue
    input_file.read(8)
    input_file.read(8)
    data5=input_file.read(4)
    group_string_length = struct.unpack(">I", data5)

    input_file.read(group_string_length[0])
    if group_string_length[0] > 0:
        group_string=struct.unpack(">c", data5)
        print(group_string)
    data7=input_file.read(48)


    #reading bytes?
    import os
    size = os.path.getsize(input_file_name)
    s = size -(77+(2*metrics_list_array_size[0])+(group_string_length[0])+xx)   #Not sure if the xx will work for all cases.. in this case is 69
    record_length = s/record_size[0]

    cols = ['Record Number', 'Timestamp (ms)', 'State', 'Activity Level', 'Movr Frame', 'cXmm', 'Speed_Av_mm_per_sec', 'Heading_deg', 'cYmm', 'Error_code'] #Will need to change the metric names if they change
    lst = []
    
    from tqdm import tqdm
    for n in tqdm(range(0,int(record_length))):
        data7=input_file.read(4)
        ms_time=struct.unpack(">I", data7)

        data8=input_file.read(1)
        state=struct.unpack(">B",data8)
        if state[0] == 0:
            x="Unknown"
        elif state[0] == 1:
            x="Locomotive"
        elif state[0] == 2:
            x="Stationary"
        elif state[0]== 3:
            x="Stationary Static"
        elif state[0]==4:
            x="Stationary Active"
        else:
            raise ValueError("Unknown state value: {}".format(state[0]))

        data9 = input_file.read(2)
        activity_level=struct.unpack(">H",data9)

        data10 = input_file.read(4)
        movr_frame=struct.unpack(">I", data10)

        data11 = input_file.read(4)
        metrics_array_size=struct.unpack(">I", data11)

        data12 = input_file.read(4*metrics_array_size[0])
        a =">"+str(metrics_array_size[0])+"f"
        metrics_array=struct.unpack(a, data12)
        lst.append([n, ms_time[0], x, activity_level[0], movr_frame[0], metrics_array[0], metrics_array[1], metrics_array[2], metrics_array[3], metrics_array[4]])

    df1 = pd.DataFrame(lst, columns=cols)

    if unique_adj==True:
        df1['cXmm']=df1['cXmm'] * (1/68) * 6.4
        df1['cYmm']=df1['cYmm'] * (1/68) * 6.4
        df1['Speed_Av_mm_per_sec']=df1['Speed_Av_mm_per_sec'] * (1/68) * 6.4

    if model != None:
        nums=[1] if fps==10 else [1,2,3,4,5]
        for n in nums:
            df1['Activity Level_prior'+str(n)] = df1['Activity Level'].shift(n)
            df1['Speed_prior'+str(n)] = df1['Speed_Av_mm_per_sec'].shift(n)
        df1 = df1.dropna().copy()
        if fps == 10:
            y_pred = model.predict(df1.loc[:,('Speed_Av_mm_per_sec','Activity Level', 'Activity Level_prior1','Speed_prior1')])
        else:
            y_pred = model.predict(df1.loc[:,('Speed_Av_mm_per_sec','Activity Level', 'Activity Level_prior1','Speed_prior1','Activity Level_prior2','Speed_prior2','Activity Level_prior3','Speed_prior3','Activity Level_prior4','Speed_prior4','Activity Level_prior5','Speed_prior5')])
        df1['New_state'] = y_pred

        df1.loc[(df1['State'] =='Stationary Static'), ['Old_State']] = 1
        df1.loc[(df1['State'] =='Stationary Active'), ['Old_State']] = 2
        df1.loc[(df1['State'] =='Locomotive'), ['Old_State']] = 3

        df1=df1.loc[:,('Record Number','Timestamp (ms)','Movr Frame','Error_code','cXmm', 'cYmm','Heading_deg','Activity Level','Speed_Av_mm_per_sec','Old_State','New_state')].reset_index().copy()

    if output == None:
        return df1
    else:
        df1.to_csv(output)

# Defines function to convert all idx files in a folder to csv files in another folder. Just specify input and output folder paths in following cell.
def idx_to_csv(input, output, custom_name=None):
    import os
    for filename in os.listdir(input):
        if filename.endswith(".idx") and not filename.startswith('._'):
            # Get the base filename without extension
            base_name = filename.split(".")[0]
            
            if custom_name is not None:
                date_prefix = base_name.split(" ")[0]
                number_suffix = base_name.split("_")[-1]
                new_filename = f"{date_prefix} {custom_name}_{number_suffix}.csv"
            else:
                new_filename = f"{base_name}.csv"
            
            IndexToCSV(file = os.path.join(input, filename), model=None, fps=10,
                        output = os.path.join(output, new_filename)
            )
            
def process_genotype_data(folder_path, time_filter=None, max_time=180, bin_size=None):
    import pandas as pd
    import glob
    import os
    import numpy as np
    """
    Process all CSV files in a folder to create combined dataframe with both Activity Level and Speed metrics
    
    Parameters:
    -----------
    folder_path : str
        Path to folder containing CSV files
    time_filter : str, optional
        Time filter pattern (e.g., "5s")
    max_time : int
        Maximum time to include in analysis (seconds)
        
    Returns:
    --------
    pd.DataFrame
        Combined dataframe with time as index and metrics_flynumber as columns
    """
    
    # Find all CSV files
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    if not csv_files:
        print(f"No CSV files found in {folder_path}")
        return None
    
    # Filter files by time parameter if specified
    if time_filter:
        time_pattern = f"_{time_filter}_"
        csv_files = [f for f in csv_files if time_pattern in os.path.basename(f)]
        print(f"Time filter '{time_filter}' applied: {len(csv_files)} files found")
    
    if not csv_files:
        print(f"No CSV files found with time filter '{time_filter}' in {folder_path}")
        return None

    # Process each file
    all_dataframes = []
    
    for i, file in enumerate(csv_files, start=1):
        try:
            # Read CSV file with both metrics
            df = pd.read_csv(file, usecols=["Timestamp (ms)", "Activity Level", "Speed_Av_mm_per_sec"])
            
            # Convert timestamps to seconds starting from 0
            df["Time (s)"] = (df["Timestamp (ms)"] - df["Timestamp (ms)"].iloc[0]) / 1000
            df = df.set_index("Time (s)")
            
            # Limit time range
            df = df[df.index <= max_time]
            
            # Create individual dataframe for this fly
            fly_df = pd.DataFrame(index=df.index)
            fly_df[f"ActivityLevel_{i}"] = df["Activity Level"]
            fly_df[f"Speed_{i}"] = df["Speed_Av_mm_per_sec"]
            
            all_dataframes.append(fly_df)
            
        except Exception as e:
            print(f"Error processing file {os.path.basename(file)}: {e}")
            continue
    
    if not all_dataframes:
        print("No valid data processed")
        return None
    
    # Concatenate all individual dataframes
    combined_df = pd.concat(all_dataframes, axis=1)
    
    # Group by time bins and calculate mean
    binned_df = combined_df.groupby((combined_df.index // bin_size) * bin_size).mean()
    
    # Log10 transform Activity Level columns and rename
    activity_cols = [col for col in binned_df.columns if col.startswith("ActivityLevel")]
    
    for col in activity_cols:
        # Create log10 transformed column
        fly_num = col.split("_")[1]  # Extract fly number
        log_col_name = f"ActivityLevelLog10_{fly_num}"
        binned_df[log_col_name] = np.log10(binned_df[col] + 1)
        
        # Drop original activity level column
        binned_df.drop(columns=[col], inplace=True)
   
    return binned_df

