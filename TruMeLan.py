#Data is big endian format so have to use >... for datatype (eg >I) for unsigned integer

def MovrHeader(file):
    """
    Function for reading and outputting the header of a movr file

    Parameters
    ----------
    file : Str
        The .movr file input.

    Returns
    -------
    df1 : DataFrame
        A dataframe of the movrheader information.

    """
    import struct
    import pandas as pd
    input_file_name = (file)
    input_file = open(input_file_name, 'rb')                                   #Have to specify 'rb' for readbytes rather than writing a file
    data = input_file.read(1)
    data1 = input_file.read(16)
    filetype_version = struct.unpack("B", data)
    header = struct.unpack(">4i", data1)
    header_length= input_file.tell() #.tell() function shows you how many bytes have been read so far
    cols = ['Filetype_Version', 'Header_Version', 'Image_Xres', 'Image_Yres', 'Record_Size', 'Header_Length']
    lst = []
    lst.append([filetype_version[0], header[0], header[1], header[2],header[3], header_length])
    df1 = pd.DataFrame(lst, columns=cols)
    return df1

def MovrRecordSelector(file, s,f):
    """
    A function that selects and prints the records in the .movr file given your selection

    Parameters
    ----------
    file : Str
        The input .movr file.
    s : Int
        The start frame.
    f : Int
        The final frame.

    Returns
    -------
    df1 : DataFrame
        A dataframe with each row as a record for the records selected.

    """
    
    from matplotlib import pyplot as plt
    import numpy as np
    import struct
    from datetime import datetime
    import pandas as pd
    input_file_name = (file)
    input_file = open(input_file_name, 'rb')
    data = input_file.read(1)
    data1 = input_file.read(16)
    struct.unpack("B", data)
    header = struct.unpack(">4i", data1)
    input_file.tell() #.tell() function shows you how many bytes have been read so far
    
    cols = ['Record Number', 'Frame Number', 'Timestamp (ms)', 'DateTime', 'Error_code', 'Areapix', 'cXpix', 'cYpix',
           'Orientation','Top_pix','Bounding_Diag','Axis_X1','Axis_Y1','Axis_X2','Axis_Y2','cXmm','cX','cYmm','cY',
           'Top_mm','Vx_mm_per_sec','Vy_mm_per_sec','Orbital_deg','Orbital_radius','Orbital_deg_per_sec','Noise_level','Vx_Av_mm_per_sec','Vy_Av_mm_per_sec','W_Av_deg_per_sec',
           'Track_deg','Speed_mm_per_sec','Speed_Av_mm_per_sec','dXmm','dYmm','distance_mm','Heading_deg','HeadingConf','Length','HeadX_pix','HeadY_pix']
    lst = []

    input_file.seek(header[3]*s, 1)                                            #This function will skip through to the first record you are actually interested in
    for n in range(s,f):                                                       #For loop here allows to loop through one record at a time
        
        data2 = input_file.read(4)
        frame_num = struct.unpack(">I", data2)
        
        data3 = input_file.read(4)
        ms_time = struct.unpack(">I", data3)
        
        data4 = input_file.read(8)
        ab_time = struct.unpack(">q", data4)
        timestamp = ab_time[0]-2082816000
       
        data4b=input_file.read(8)
        fraction = struct.unpack(">Q", data4b)
        time = timestamp + (fraction[0] * pow(2, -64))
        unix_val = datetime.utcfromtimestamp(time)
        
        data5 = input_file.read(4)
        metric_array_size =struct.unpack(">I", data5)
        m_array_size = metric_array_size[0]
        
        data6=input_file.read(4*m_array_size)
        x=">"+str(m_array_size)+"f"
        metrics_array =struct.unpack(x, data6)
    
        data7= input_file.read(4)
        image_num_row= struct.unpack(">I", data7)
    
        data8= input_file.read(4)
        image_num_col= struct.unpack(">I", data8)
        
        image_array= np.empty(shape=(image_num_row[0], image_num_col[0]), dtype=int)
        for i in range(0, image_num_row[0]):
            for j in range(0, image_num_col[0]):
                data=input_file.read(1)
                image_array[i,j] = struct.unpack(">B", data)[0]                #Read one byte at a time and place into a 2d array -> creates the image once plotted
        print("Image for Record: " + str(n))
        plt.imshow(image_array, interpolation='nearest')
        plt.gray()                                                             #Required for the plot to use grayscale rather than a heatmap looking style
        plt.show()    
        print("--------------------------------------------------")
        lst.append([n, frame_num[0], ms_time[0], unix_val, metrics_array[0], metrics_array[1], metrics_array[2], metrics_array[3], metrics_array[4],metrics_array[5],
                   metrics_array[6],metrics_array[7],metrics_array[8],metrics_array[9],metrics_array[10],metrics_array[11],metrics_array[12],metrics_array[13],metrics_array[14]
                   ,metrics_array[15],metrics_array[16],metrics_array[17],metrics_array[18],metrics_array[19],metrics_array[20],metrics_array[21],metrics_array[22],metrics_array[23],
                   metrics_array[24],metrics_array[25],metrics_array[26],metrics_array[27],metrics_array[28],metrics_array[29],metrics_array[30],metrics_array[31],metrics_array[32],
                   metrics_array[33],metrics_array[34],metrics_array[35]])
        
    df1 = pd.DataFrame(lst, columns=cols)   
    return df1
        

def ImageSelector(file, s,f):
    """
    Saves images for the deisred records

    Parameters
    ----------
    file : Str
        The input file.
    s : Int
        The first record.
    f : Int
        The final record.

    Returns
    -------
    None.
    
    Outputs
    -------
    .png images
    """
    
    import matplotlib.pyplot as plt
    plt.gray()
    plt.ioff()
    from matplotlib import pyplot as plt
    import numpy as np
    import struct
    input_file_name = (file)

    input_file = open(input_file_name, 'rb')
    data = input_file.read(1)
    data1 = input_file.read(16)
    header = struct.unpack(">4i", data1)
    
    input_file.seek(header[3]*s, 1)
    
    from tqdm import tqdm
    for n in tqdm(range(s, f)):
        
        input_file.read(24)
        
        data5 = input_file.read(4)
        metric_array_size =struct.unpack(">I", data5)
        m_array_size = metric_array_size[0]

        input_file.read(4*m_array_size)

        data7= input_file.read(4)
        image_num_row= struct.unpack(">I", data7)

        data8= input_file.read(4)
        image_num_col= struct.unpack(">I", data8)

        image_array= np.empty(shape=(image_num_row[0], image_num_col[0]), dtype=int)
        for i in range(0, image_num_row[0]):
            for j in range(0, image_num_col[0]):
                data=input_file.read(1)
                image_array[i,j] = struct.unpack(">B", data)[0]
    
        plt.imshow(image_array, interpolation='nearest')
        name="Images\\image"+str(n)+".png"
        plt.savefig(name)
        plt.close()
        #plt.show()

#A function to output the .movr file details (excluding the 2d image array) into a csv file
def MovrToCSV(file,output):
    """

    Parameters
    ----------
    file : Str
        Input .movr file.
    output : Str
        Desired output file .csv location.

    Returns
    -------
    None.
    
    Outputs
    -------
    CSV file
    """
    
    import numpy as np
    import pandas as pd
    import struct
    from datetime import datetime
    input_file_name = (file)
    
    input_file = open(input_file_name, 'rb')
    data = input_file.read(1)
    data1 = input_file.read(16)
    header = struct.unpack(">4i", data1)
    header_length= input_file.tell()
    
    
    cols = ['Record Number', 'Frame Number', 'Timestamp (ms)', 'DateTime', 'Error_code', 'Areapix', 'cXpix', 'cYpix',
           'Orientation','Top_pix','Bounding_Diag','Axis_X1','Axis_Y1','Axis_X2','Axis_Y2','cXmm','cX','cYmm','cY',
           'Top_mm','Vx_mm_per_sec','Vy_mm_per_sec','Orbital_deg','Orbital_radius','Orbital_deg_per_sec','Noise_level','Vx_Av_mm_per_sec','Vy_Av_mm_per_sec','W_Av_deg_per_sec',
           'Track_deg','Speed_mm_per_sec','Speed_Av_mm_per_sec','dXmm','dYmm','distance_mm','Heading_deg','HeadingConf','Length','HeadX_pix','HeadY_pix']
    lst = []
    
    #reading bytes?
    import os
    size = os.path.getsize(input_file_name)
    s = size - header_length
    record_length = s/header[3]
    
    from tqdm import tqdm
    for n in tqdm(range(0,int(record_length))):
        
        data2 = input_file.read(4)
        frame_num = struct.unpack(">I", data2)
        
        data3 = input_file.read(4)
        ms_time = struct.unpack(">I", data3)
        
        data4 = input_file.read(8)
        ab_time = struct.unpack(">q", data4)
        timestamp = ab_time[0]-2082816000
       
        data4b=input_file.read(8)
        fraction = struct.unpack(">Q", data4b)
        time = timestamp +(fraction[0] * pow(2, -64))
        unix_val = datetime.utcfromtimestamp(time)
            
        data5 = input_file.read(4)
        metric_array_size =struct.unpack(">I", data5)
        m_array_size = metric_array_size[0]
        
        data6=input_file.read(4*m_array_size)
        x=">"+str(m_array_size)+"f"
        metrics_array =struct.unpack(x, data6)
    
        data7= input_file.read(4)
        image_num_row= struct.unpack(">I", data7)
    
        data8= input_file.read(4)
        image_num_col= struct.unpack(">I", data8)
        
        image_array= np.empty(shape=(image_num_row[0], image_num_col[0]), dtype=int)
        for i in range(0, image_num_row[0]):
            for j in range(0, image_num_col[0]):
                data=input_file.read(1)
                image_array[i,j] = struct.unpack(">B", data)[0]  
            
        lst.append([n, frame_num[0], ms_time[0], unix_val, metrics_array[0], metrics_array[1], metrics_array[2], metrics_array[3], metrics_array[4],metrics_array[5],
                   metrics_array[6],metrics_array[7],metrics_array[8],metrics_array[9],metrics_array[10],metrics_array[11],metrics_array[12],metrics_array[13],metrics_array[14]
                   ,metrics_array[15],metrics_array[16],metrics_array[17],metrics_array[18],metrics_array[19],metrics_array[20],metrics_array[21],metrics_array[22],metrics_array[23],
                   metrics_array[24],metrics_array[25],metrics_array[26],metrics_array[27],metrics_array[28],metrics_array[29],metrics_array[30],metrics_array[31],metrics_array[32],
                   metrics_array[33],metrics_array[34],metrics_array[35]])
        
    df1 = pd.DataFrame(lst, columns=cols)
    df1.to_csv(output)


#A function to extract and print the Index file header
def IndexHeader(file, Video=1):
    """
    Function to read and output the index file header
    Parameters
    ----------
    file : str
        Input .idx file.
    Video : int (0 or 1)
        To say if you had created movr files when doing the experiment. 
        Default is yes (1). If you hadnt, use (0)
    Returns
    -------
    df1 : DataFrame
        A dataframe containing index file header information.

    """
    
    import struct
    from datetime import datetime
    import pandas as pd
    input_file_name = (file)
    input_file = open(input_file_name, 'rb')

    print("Header:")
    data = input_file.read(1)
    filetype_version = struct.unpack(">B", data)
    print('The filetype version is:       '+str(filetype_version[0]))

    data1=input_file.read(4)
    metrics_list_array_size=struct.unpack(">I", data1)
    print('The metrics list array size:   '+str(metrics_list_array_size[0]))

    data2=input_file.read(2*metrics_list_array_size[0])
    mla=">"+str(metrics_list_array_size[0])+"H"
    metrics_list_array=struct.unpack(mla, data2)
    print('The metrics list array:        '+str(metrics_list_array))

    data3=input_file.read(4)
    record_size=struct.unpack(">i",data3)
    print('The record size:               '+str(record_size[0]))

    if Video==1:    
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
    elif Video==0:
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
        
    data4 = input_file.read(8)
    ab_time = struct.unpack(">q", data4)
    timestamp = ab_time[0]-2082816000
    data4b=input_file.read(8)
    fraction = struct.unpack(">Q", data4b)
    time = timestamp + (fraction[0] * pow(2, -64))
    unix_val = datetime.utcfromtimestamp(time)
    
    print('The absolute timestamp is:     '+str(ab_time[0]))
    print('The fraction is:               '+str(fraction[0]))
    print('The unix time is:              '+str(timestamp))  
    print("DateTime:                     ",unix_val)

    data5=input_file.read(4)
    group_string_length = struct.unpack(">I", data5)
    print("The group string length:       "+str(group_string_length[0]))

    input_file.read(group_string_length[0])
    if group_string_length[0] > 0:
        group_string=struct.unpack(">c", data5)
        print(group_string)
        
    #reading bytes?
    import os
    size = os.path.getsize(input_file_name)
    print("The total size is:             " +str(size))
    s = size -(77+(2*metrics_list_array_size[0])+(group_string_length[0])+xx)   #Not sure if the xx will work for all cases.. in this case is 69
    print("The size minus header:         " +str(s))
    record_length = s/record_size[0]
    print("The number of records is:      "+str(record_length))
    print("------------------------------------------------") 
    metrics=['Error_code', 'Areapix', 'cXpix', 'cYpix',
           'Orientation','Top_pix','Bounding_Diag','Axis_X1','Axis_Y1','Axis_X2','Axis_Y2','cXmm','cX','cYmm','cY',
           'Top_mm','Vx_mm_per_sec','Vy_mm_per_sec','Orbital_deg','Orbital_radius','Orbital_deg_per_sec','Noise_level','Vx_Av_mm_per_sec','Vy_Av_mm_per_sec','W_Av_deg_per_sec',
           'Track_deg','Speed_mm_per_sec','Speed_Av_mm_per_sec','dXmm','dYmm','distance_mm','Heading_deg','HeadingConf','Length','HeadX_pix','HeadY_pix']
    m1=metrics[(metrics_list_array[0])]
    m2=metrics[(metrics_list_array[1])]
    m3=metrics[(metrics_list_array[2])]
    m4=metrics[(metrics_list_array[3])]
    m5=metrics[(metrics_list_array[4])]
    cols = ['Filetype_Version', 'DateTime', 'Record_Size', 'Number_of_Records', 'Metric1', 'Metric2', 'Metric3', 'Metric4', 'Metric5']
    lst = []
    lst.append([filetype_version[0], unix_val, record_size[0],  record_length, m1, m2, m3,m4,m5])
    df1 = pd.DataFrame(lst, columns=cols)
    return df1    

def HeaderVariables(file, Video=1):
    """
    Function to read and output the index file header
    Parameters
    ----------
    file : str
        Input .idx file.
    Video : int (0 or 1)
        To say if you had created movr files when doing the experiment. 
        Default is yes (1). If you hadnt, use (0)
    Returns
    -------
    df1 : DataFrame
        A dataframe containing index file header information.

    """
    
    import struct
    input_file_name = (file)
    input_file = open(input_file_name, 'rb')

    input_file.read(1)

    data1=input_file.read(4)
    metrics_list_array_size=struct.unpack(">I", data1)

    input_file.read(2*metrics_list_array_size[0])

    data3=input_file.read(4)
    record_size=struct.unpack(">i",data3)


    if Video==1:    
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
    elif Video==0:
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

    headlen=(77+(2*metrics_list_array_size[0])+(group_string_length[0])+xx)
    return headlen, record_size[0]

def IndexRecordSelector(file,start,f, Video=1):
    """
    A function to extract and print the desired records from the index file
    
    Parameters
    ----------
    file : Str
        Input .idx file.
    start : Int
        Start frame.
    f : Int
        End frame.
    Video : int (0 or 1)
        To say if you had created movr files when doing the experiment. 
        Default is yes (1). If you hadnt, use (0)
    Returns
    -------
    df1 : DataFrame
        Output dataframe with each row as a record/frame from the index file.

    """
    
    #INDEX FILE
    import struct
    from datetime import datetime
    import pandas as pd
    input_file_name = (file)
    input_file = open(input_file_name, 'rb')
    
    print("Header:")
    data = input_file.read(1)
    filetype_version = struct.unpack(">B", data)
    print('The filetype version is:       '+str(filetype_version[0]))
    
    data1=input_file.read(4)
    metrics_list_array_size=struct.unpack(">I", data1)
    print('The metrics list array size:   '+str(metrics_list_array_size[0]))
    
    data2=input_file.read(2*metrics_list_array_size[0])
    mla=">"+str(metrics_list_array_size[0])+"H"
    metrics_list_array=struct.unpack(mla, data2)
    print('The metrics list array:        '+str(metrics_list_array))
    
    data3=input_file.read(4)
    record_size=struct.unpack(">i",data3)
    print('The record size:               '+str(record_size[0]))
    
    if Video==1:    
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
    elif Video==0:
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
    data4 = input_file.read(8)
    ab_time = struct.unpack(">q", data4)
    timestamp = ab_time[0]-2082816000
    data4b=input_file.read(8)
    fraction = struct.unpack(">Q", data4b)
    time = timestamp + (fraction[0] * pow(2, -64))
    unix_val = datetime.utcfromtimestamp(time)  
    print("DateTime:                     ",unix_val)
    
    data5=input_file.read(4)
    group_string_length = struct.unpack(">I", data5)
    print("The group string length:       "+str(group_string_length[0]))
    
    input_file.read(group_string_length[0])
    if group_string_length[0] > 0:
        group_string=struct.unpack(">c", data5)
        print(group_string)
    data7=input_file.read(48)
    
    
    #reading bytes?
    import os
    size = os.path.getsize(input_file_name)
    print("The total size is:             " +str(size))
    s = size -(77+(2*metrics_list_array_size[0])+(group_string_length[0])+xx)   #Not sure if the xx will work for all cases.. in this case is 69
    print("The size minus header:         " +str(s))
    record_length = s/record_size[0]
    print("The number of records is:      "+str(record_length))
    
    print("------------------------------------------------")
    input_file.seek(record_size[0]*start, 1)
    
    cols = ['Record Number', 'Timestamp (ms)', 'State', 'Activity Level', 'Movr Frame', 'cXmm', 'Speed_Av_mm_per_sec', 'Heading_deg', 'cYmm', 'Error_code'] #Will need to change the metric names if they change
    lst = []
    
    for n in range(start,f):
        
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
    return df1
        
def IndexToCSV(file,output, Video=1):
    """
    A function to convert the whole index file (excluding the header) to a csv

    Parameters
    ----------
    file : Str
        Input .idx file location
    output : Str
        Output .csv file location  
    Video : int (0 or 1)
        To say if you had created movr files when doing the experiment. 
        Default is yes (1). If you hadnt, use (0)
    Returns
    -------
    None.
    
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

    if Video==1:    
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
    elif Video==0:
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
    df1.to_csv(output)

def csv_read(file, fps=45):
    """
    Reading and adjusting csv input

    Parameters
    ----------
    file : Str
        Input .csv file

    Returns
    -------
    df1 : DataFrame
        Outputs a dataframe with additional columns from the .csv input

    """
    fps1=(1/fps)*1000
    import pandas as pd
    df = pd.read_csv(file)
    df['Time_ms'] = df['Timestamp (ms)'] - df.loc[0,'Timestamp (ms)']
    df.drop('Unnamed: 0', axis=1, inplace=True)
    # shift column 'Time_ms' to first position
    first_column = df.pop('Time_ms')
    df.insert(0, 'Time_ms', first_column)
    df1 = df.copy()

    #Separates each bout of state. The 'e5' column provides the number corresponding to the bout.
    df1["e3"] = df1["State"].shift(1)
    df1["e4"] = df1["State"] != df1["e3"]
    df1["e5"] = df1["e4"].cumsum()
    df1["e6"] = df1.Time_ms.shift(-1)   #<-This provides the time from the row below
    
    #Showing the frame & time for each bout of a state
    dft = pd.DataFrame(df1.groupby('e5').cumcount())
    df1['Bout_frame_number'] = dft.iloc[:,0]
    df1['Bout_duration_rough'] = (df1['Bout_frame_number'] * fps1) + fps1
    df1['Hour'] = df1['Time_ms']/3600000
    df1['Seconds'] = df1['Hour'] * 3600
    df1['Minutes'] = df1['Seconds']/60
    return df1

def csv_read_trim(file):
    """
    Reading and adjusting csv input

    Parameters
    ----------
    file : Str
        Input .csv file

    Returns
    -------
    df1 : DataFrame
        Outputs a dataframe with additional columns from the .csv input

    """
    
    import pandas as pd
    df = pd.read_csv(file)
    df['Time_ms'] = df['Timestamp (ms)'] - df.loc[0,'Timestamp (ms)']
    df.drop('Unnamed: 0', axis=1, inplace=True)
    # shift column 'Time_ms' to first position
    first_column = df.pop('Time_ms')
    df.insert(0, 'Time_ms', first_column)

    #Separates each bout of state. The 'e5' column provides the number corresponding to the bout.
    df["e3"] = df["State"].shift(1)
    df["e4"] = df["State"] != df["e3"]
    df["e5"] = df["e4"].cumsum()
    df["e6"] = df.Time_ms.shift(-1)   #<-This provides the time from the row below
    
    #Showing the frame & time for each bout of a state
    dft = pd.DataFrame(df.groupby('e5').cumcount())
    df['Bout_frame_number'] = dft.iloc[:,0]
    df['Bout_duration_rough'] = (df['Bout_frame_number'] * 22.2222222) + 22.2222222
    df['Hour'] = df['Time_ms']/3600000
    df['Seconds'] = df['Hour'] * 3600
    df['Minutes'] = df['Seconds']/60
    df = df.loc[:, ['Time_ms','e5', 'cYmm', 'State','e6', 'Bout_frame_number', 'Bout_duration_rough']]
    return df


def cYmm_bottom_selector(dfi, tt):
    """
    

    Parameters
    ----------
    dfi : dataframe 
        Input dataframe.
    tt : int
        The SS bout threshold.
    n  : int
        The location you want to record cYmm from
        Default is the final height: -1
        Start height would be: 0

    Returns
    -------
    df : dataframe 
        Output dataframe.

    """
    df2_gbmax = dfi.groupby(['e5', 'State', 'Fly'])[['e6']].max()
    df2_gbmin = dfi.groupby(['e5', 'State', 'Fly'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3['Seconds'] = df3['Time']/1000
    df3['sY'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(0)
    df3['eY'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(-1)
    df=df3.reset_index()
    df = df[df['State'].isin(['Stationary Static'])]
    df = df[df['Seconds'] > tt]
    df = df[df['eY'] >= 1.9]
    df = df[df['sY'] >= 1.9]
    df['deY'] =  3.5 - df['eY']
    df['dsY'] =  3.5 - df['sY']
    return df

def cYmm_top_selector(dfi, tt):
    """
    

    Parameters
    ----------
    dfi : dataframe 
        Input dataframe.
    tt : int
        The SS bout threshold.
    n  : int
        The location you want to record cYmm from
        Default is the final height: -1
        Start height would be: 0
    Returns
    -------
    df : dataframe 
        Output dataframe.

    """
    df2_gbmax = dfi.groupby(['e5', 'State', 'Fly'])[['e6']].max()
    df2_gbmin = dfi.groupby(['e5', 'State', 'Fly'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3['Seconds'] = df3['Time']/1000
    df3['sY'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(0)
    df3['eY'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(-1)
    df=df3.reset_index()
    df = df[df['State'].isin(['Stationary Static'])]
    df = df[df['Seconds'] > tt]
    df = df[df['eY'] < 1.9]
    df = df[df['sY'] < 1.9]
    df['deY'] =  df['eY']
    df['dsY'] =  df['sY']
    return df

def Ypos_Start_End(df1,df2):
    import pandas as pd
    ground = df1[df1['dsY'] > 0.5].copy()
    ceiling = df2[df2['dsY'] > 0.5].copy()
    ceiling['Position'] = 'Ceiling'
    ground['Position'] = 'Ground'

    ceiling_long = ceiling[ceiling['Seconds'] > 60].copy()
    ceiling_long['Duration'] = 'Long'
    ceiling_short = ceiling[(ceiling['Seconds'] > 1) & (ceiling['Seconds'] < 3)].copy()
    ceiling_short['Duration'] = 'Short'
    Ceiling = pd.concat([ceiling_short, ceiling_long], ignore_index=True)
    ground_long = ground[ground['Seconds'] > 60].copy()
    ground_long['Duration'] = 'Long'
    ground_short = ground[(ground['Seconds'] > 1) & (ground['Seconds'] < 3)].copy()
    ground_short['Duration'] = 'Short'
    Ground = pd.concat([ground_short, ground_long], ignore_index=True)


    Ground_start=Ground.loc[:,("dsY", "Position", "Duration", 'e8')]
    Ceiling_start=Ceiling.loc[:,("dsY","Position", "Duration", 'e8')]
    Ground_start.rename(columns={'dsY':'Y'}, inplace=True)
    Ceiling_start.rename(columns={'dsY':'Y'}, inplace=True)
    Ground_end=Ground.loc[:,("deY", "Position", "Duration", 'e8')]
    Ceiling_end=Ceiling.loc[:,("deY","Position", "Duration", 'e8')]
    Ground_end.rename(columns={'deY':'Y'}, inplace=True)
    Ceiling_end.rename(columns={'deY':'Y'}, inplace=True)

    Ground_start['Y-Pos'] = 'Start'
    Ceiling_start['Y-Pos'] = 'Start'
    Ground_end['Y-Pos'] = 'End'
    Ceiling_end['Y-Pos'] = 'End'
    Ground_start['ID'] = Ground_start.index
    Ceiling_start['ID'] = Ceiling_start.index
    Ground_end['ID'] = Ground_end.index
    Ceiling_end['ID'] = Ceiling_end.index

    Ground_all = pd.concat([Ground_end, Ground_start], ignore_index=True)
    Ceiling_all = pd.concat([Ceiling_end,Ceiling_start], ignore_index=True)
    Ceiling_all.sort_values(['ID', "Y-Pos"], ascending=(True, False), inplace=True)
    Ground_all.sort_values(['ID', "Y-Pos"], ascending=(True, False),inplace=True)
    Ground_all.reset_index(inplace=True)
    Ceiling_all.reset_index(inplace=True)

    Ground_start_short = Ground_start[Ground_start['Duration']=='Short']
    Ground_start_long = Ground_start[Ground_start['Duration']=='Long']
    Ground_end_short = Ground_end[Ground_end['Duration']=='Short']
    Ground_end_long = Ground_end[Ground_end['Duration']=='Long']

    Ceiling_start_short = Ceiling_start[Ceiling_start['Duration']=='Short']
    Ceiling_start_long = Ceiling_start[Ceiling_start['Duration']=='Long']
    Ceiling_end_short = Ceiling_end[Ceiling_end['Duration']=='Short']
    Ceiling_end_long =Ceiling_end[Ceiling_end['Duration']=='Long']

    Ground_start_short = Ground_start_short.groupby(['e8']).mean().reset_index()
    Ground_start_long = Ground_start_long.groupby(['e8']).mean().reset_index()
    Ground_start_short['Duration'] = 'Short'
    Ground_start_long['Duration'] = 'Long'
    Ground_start_short['Position'] = 'Ground'
    Ground_start_long['Position'] = 'Ground'
    Ground_start_short['Y-Pos'] = 'Start'
    Ground_start_long['Y-Pos'] = 'Start'

    Ground_end_short = Ground_end_short.groupby(['e8']).mean().reset_index()
    Ground_end_long = Ground_end_long.groupby(['e8']).mean().reset_index()
    Ground_end_short['Duration'] = 'Short'
    Ground_end_long['Duration'] = 'Long'
    Ground_end_short['Position'] = 'Ground'
    Ground_end_long['Position'] = 'Ground'
    Ground_end_short['Y-Pos'] = 'End'
    Ground_end_long['Y-Pos'] = 'End'

    Ceiling_start_short = Ceiling_start_short.groupby(['e8']).mean().reset_index()
    Ceiling_start_long = Ceiling_start_long.groupby(['e8']).mean().reset_index()
    Ceiling_start_short['Duration'] = 'Short'
    Ceiling_start_long['Duration'] = 'Long'
    Ceiling_start_short['Position'] = 'Ceiling'
    Ceiling_start_long['Position'] = 'Ceiling'
    Ceiling_start_short['Y-Pos'] = 'Start'
    Ceiling_start_long['Y-Pos'] = 'Start'

    Ceiling_end_short = Ceiling_end_short.groupby(['e8']).mean().reset_index()
    Ceiling_end_long = Ceiling_end_long.groupby(['e8']).mean().reset_index()
    Ceiling_end_short['Duration'] = 'Short'
    Ceiling_end_long['Duration'] = 'Long'
    Ceiling_end_short['Position'] = 'Ceiling'
    Ceiling_end_long['Position'] = 'Ceiling'
    Ceiling_end_short['Y-Pos'] = 'End'
    Ceiling_end_long['Y-Pos'] = 'End'

    Ground_START = pd.concat([Ground_start_short,Ground_start_long], ignore_index=True)
    Ceiling_START = pd.concat([Ceiling_start_short,Ceiling_start_long], ignore_index=True)
    Ground_END = pd.concat([Ground_end_short,Ground_end_long], ignore_index=True)
    Ceiling_END = pd.concat([Ceiling_end_short,Ceiling_end_long], ignore_index=True)

    Ground_START['ID'] = Ground_START.index
    Ground_END['ID'] = Ground_END.index
    Ceiling_START['ID'] = Ceiling_START.index
    Ceiling_END['ID'] = Ceiling_END.index

    Ceiling_ALL = pd.concat([Ceiling_END,Ceiling_START], ignore_index=True)
    Ground_ALL = pd.concat([Ground_END,Ground_START], ignore_index=True)

    Ceiling_ALL.sort_values(['ID', "Y-Pos"], ascending=(True, False), inplace=True)
    Ground_ALL.sort_values(['ID', "Y-Pos"], ascending=(True, False),inplace=True)
    return Ground_ALL,Ceiling_ALL



#cYmm OVER FIRST 300SECONDS IN LONG REST BOUTS
def cYmm_300s_bottom_selector(dfi, tt=300000):
    """
    

    Parameters
    ----------
    dfi : dataframe 
        Input dataframe.

    Returns
    -------
    df : dataframe 
        Output dataframe.

    """
    df2_gbmax = dfi.groupby(['e5', 'State'])[['e6']].max() 
    df2_gbmin = dfi.groupby(['e5', 'State'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3=df3.reset_index()
    df3 = df3[df3['Time']>tt]
    df3 = df3[df3['State'].isin(['Stationary Static'])]
    BoutList = df3['e5'].tolist()
    df1 = dfi.loc[:, ['e5', 'cYmm', 'Bout_frame_number', 'Bout_duration_rough', 'Fly']]
    df = df1.query('e5 in @BoutList')
    df = df[df['cYmm'] >= 1.9]
    return df
   

#cYmm OVER FIRST 300SECONDS IN LONG REST BOUTS
def cYmm_300s_top_selector(dfi,tt=300000):
    """
    

    Parameters
    ----------
    dfi : dataframe 
        Input dataframe.

    Returns
    -------
    df : dataframe 
        Output dataframe.

    """
    df2_gbmax = dfi.groupby(['e5', 'State'])[['e6']].max() 
    df2_gbmin = dfi.groupby(['e5', 'State'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3=df3.reset_index()
    df3 = df3[df3['Time']>tt]
    df3 = df3[df3['State'].isin(['Stationary Static'])]
    BoutList = df3['e5'].tolist()
    df1 = dfi.loc[:, ['e5', 'cYmm', 'Bout_frame_number', 'Bout_duration_rough', 'Fly']]
    df = df1.query('e5 in @BoutList')
    df = df[df['cYmm'] < 1.9]
    return df


def cYmm_bottom_selector_test(dfi,a,b):
    """
    

    Parameters
    ----------
    dfi : dataframe 
        Input dataframe.

    Returns
    -------
    df : dataframe 
        Output dataframe.

    """
    df2_gbmax = dfi.groupby(['e5', 'State'])[['e6']].max() 
    df2_gbmin = dfi.groupby(['e5', 'State'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3=df3.reset_index()
    df3 = df3[(df3['Time']>a) & (df3['Time']<b)]
    df3 = df3[df3['State'].isin(['Stationary Static'])]
    BoutList = df3['e5'].tolist()
    df1 = dfi.loc[:, ['e5', 'cYmm', 'Bout_frame_number', 'Bout_duration_rough', 'Fly']]
    df = df1.query('e5 in @BoutList')
    df = df[df['cYmm'] >= 1.9]
    return df
   

#cYmm OVER FIRST 300SECONDS IN LONG REST BOUTS
def cYmm_top_selector_test(dfi,a,b):
    """
    

    Parameters
    ----------
    dfi : dataframe 
        Input dataframe.

    Returns
    -------
    df : dataframe 
        Output dataframe.

    """
    df2_gbmax = dfi.groupby(['e5', 'State'])[['e6']].max() 
    df2_gbmin = dfi.groupby(['e5', 'State'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3=df3.reset_index()
    df3 = df3[(df3['Time']>a) & (df3['Time']<b)]
    df3 = df3[df3['State'].isin(['Stationary Static'])]
    BoutList = df3['e5'].tolist()
    df1 = dfi.loc[:, ['e5', 'cYmm', 'Bout_frame_number', 'Bout_duration_rough', 'Fly']]
    df = df1.query('e5 in @BoutList')
    df = df[df['cYmm'] < 1.9]
    return df



def cYmm_dadd(dft):
    import pandas as pd
    from tqdm import tqdm
    df3 = dft.groupby(['e5'])[['cYmm']].nth(0)
    dft_cY=df3.reset_index()
    e5_list = dft_cY['e5'].tolist()
    cYmm_list = dft_cY['cYmm'].tolist()
    data = pd.DataFrame()
    for (a, b) in tqdm(zip(e5_list, cYmm_list)):
        df = dft[dft['e5'] ==a].copy()
        df['Y'] = df['cYmm'] - b
        data = pd.concat([data, df], ignore_index=True)
    return data
    


def cYmm_setup(df, sec, pos):
    
    trim = df.groupby(['e5'])['cYmm'].nth(0).reset_index()
    if pos=='bot':
        BoutList = trim[trim['cYmm'] >=2.4]['e5'].to_list()
    elif pos=='top':
        BoutList = trim[trim['cYmm'] <=1.5]['e5'].to_list()
    else:
        raise ValueError('Choose "bot" or "top" ')
    df = df.query('e5 in @BoutList').copy()
    
    
    y = df.groupby(['e5'])['Y'].nth(3).reset_index()
    BoutList = y[y['Y']!=0.0]['e5'].to_list()
    df_b = df.query('e5 in @BoutList').copy()
    
    boutnum = len(df_b['e5'].unique())
    df_b['S'] = df_b['Bout_duration_rough']/1000
    df_b['M'] = df_b['S']/60
    df_b_av = df_b.groupby(['Bout_frame_number','S', 'M'])[['Y']].mean()
    df_b_av = df_b_av.reset_index()
    df_b_av['deltaY'] = df_b_av['Y'] - (df_b_av.iloc[0,3])

    df1 = df_b.groupby(['Bout_frame_number'])[['Y']].sem()
    df1 = df1.reset_index()
    df_b_av['dYSEM'] = df1['Y']
    df_b_av['dYSEM'] = df_b_av['dYSEM'] -df_b_av.iloc[0,5]
    df_b_av['dCI'] = df_b_av['dYSEM']*1.96 
    
    if sec==300:
        data = df_b_av[df_b_av['M'] < 5]
    elif sec==60:
        data = df_b_av[df_b_av['M'] < 1]
    elif sec==30:
        data = df_b_av[df_b_av['S'] < 30]
    elif sec==15:
        data = df_b_av[df_b_av['S'] < 15]
    elif sec==5:
        data = df_b_av[df_b_av['S'] < 5]
    else:
        data=df_b_av
    return data, boutnum



#Selecting SS bouts greater than 60 Seconds

def startY_long_bottom_selector(dfi, tt):
    """
    

    Parameters
    ----------
    dfi : dataframe 
        Input dataframe.
    tt : int
        The SS bout threshold.
    n  : int
        The location you want to record cYmm from
        Default is the final height: -1
        Start height would be: 0

    Returns
    -------
    df : dataframe 
        Output dataframe.

    """
    df2_gbmax = dfi.groupby(['e5', 'State', 'Fly'])[['e6']].max()
    df2_gbmin = dfi.groupby(['e5', 'State', 'Fly'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3['Seconds'] = df3['Time']/1000
    df3['cYmm'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(0)
    df=df3.reset_index()
    df = df[df['State'].isin(['Stationary Static'])]
    df = df[df['Seconds'] > tt]
    df = df[df['cYmm'] >= 1.9]
    df['deltaY'] =  3.5 - df['cYmm']
    return df

#Selecting SS bouts greater than 60 Seconds
def startY_long_top_selector(dfi, tt):
    """
    

    Parameters
    ----------
    dfi : dataframe 
        Input dataframe.
    tt : int
        The SS bout threshold.
    n  : int
        The location you want to record cYmm from
        Default is the final height: -1
        Start height would be: 0
    Returns
    -------
    df : dataframe 
        Output dataframe.

    """
    df2_gbmax = dfi.groupby(['e5', 'State', 'Fly'])[['e6']].max()
    df2_gbmin = dfi.groupby(['e5', 'State', 'Fly'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3['Seconds'] = df3['Time']/1000
    df3['cYmm'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(0)
    df=df3.reset_index()
    df = df[df['State'].isin(['Stationary Static'])]
    df = df[df['Seconds'] > tt]
    df = df[df['cYmm'] < 1.9]
    df['deltaY'] =  df['cYmm'] 
    return df



#Selecting SS bouts 1-3 Seconds

def startY_short_bottom_selector(dfi):
    """
    

    Parameters
    ----------
    dfi : dataframe 
        Input dataframe.
    tt : int
        The SS bout threshold.
    n  : int
        The location you want to record cYmm from
        Default is the final height: -1
        Start height would be: 0

    Returns
    -------
    df : dataframe 
        Output dataframe.

    """
    df2_gbmax = dfi.groupby(['e5', 'State', 'Fly'])[['e6']].max()
    df2_gbmin = dfi.groupby(['e5', 'State', 'Fly'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3['Seconds'] = df3['Time']/1000
    df3['cYmm'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(0)
    df=df3.reset_index()
    df = df[df['State'].isin(['Stationary Static'])]
    df = df[df['Seconds'] > 1]
    df = df[df['Seconds'] < 3]
    df = df[df['cYmm'] >= 1.9]
    df['deltaY'] =  3.5 - df['cYmm']
    return df

#Selecting SS bouts 1-3 Seconds
def startY_short_top_selector(dfi):
    """
    

    Parameters
    ----------
    dfi : dataframe 
        Input dataframe.
    tt : int
        The SS bout threshold.
    n  : int
        The location you want to record cYmm from
        Default is the final height: -1
        Start height would be: 0
    Returns
    -------
    df : dataframe 
        Output dataframe.

    """
    df2_gbmax = dfi.groupby(['e5', 'State', 'Fly'])[['e6']].max()
    df2_gbmin = dfi.groupby(['e5', 'State', 'Fly'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3['Seconds'] = df3['Time']/1000
    df3['cYmm'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(0)
    df=df3.reset_index()
    df = df[df['State'].isin(['Stationary Static'])]
    df = df[df['Seconds'] > 1]
    df = df[df['Seconds'] < 3]
    df = df[df['cYmm'] < 1.9]
    df['deltaY'] =  df['cYmm'] 
    return df


        
def cYmm_prerest_long_bottom_selector(dfi, tt=60000):
    import pandas as pd
    dfi=dfi.loc[:,["Time_ms","Record Number","State",  "cYmm", "e5", "e6"]]
    df2_gbmax = dfi.groupby(['e5', 'State'])[['e6']].max() 
    df2_gbmin = dfi.groupby(['e5', 'State'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df_s= dfi.groupby(['e5', 'State'])[['Record Number']].min() 
    df_e= dfi.groupby(['e5', 'State'])[['Record Number']].max() 
    df_y = dfi.groupby(['e5', 'State'])[['cYmm']].mean() 
    df3['Start_frame'] = df_s['Record Number'] 
    df3['End_frame'] =  df_e['Record Number']
    df3['cYmm'] = df_y['cYmm']
    df3 = df3.reset_index()
    df3 = df3[(df3['cYmm'] >= 1.9) & (df3['Time']>tt) & (df3['State'].isin(['Stationary Static']))]
    df3['SL_90'] = df3['Start_frame'] -90
    df3['e1'] = df3["End_frame"].shift(1)
    df3['e2'] = df3['e1'] < df3['Start_frame']
    df3 = df3[df3['e2'] ==True]
    SL = df3['SL_90'].tolist()
    EL = df3['End_frame'].tolist()   
    NM = df3['e5'].tolist()
    data = pd.DataFrame()
    for (a, b, c) in zip(SL, EL, NM):
            df = dfi.loc[a:b,].copy()
            df['new_e5'] = c
            data = pd.concat([data, df], ignore_index=True)  
    df3= data.groupby(['new_e5'])[['cYmm']].nth(0)
    df3 = df3.reset_index()
    e5_list = df3['new_e5'].tolist()
    cYmm_list = df3['cYmm'].tolist()
    dt = pd.DataFrame()
    for (a, b) in zip(e5_list, cYmm_list):
        df = data[data['new_e5'] ==a].copy()
        df['Y'] = df['cYmm'] - b
        dt = pd.concat([dt, df], ignore_index=True)

    return dt

def cYmm_prerest_long_top_selector(dfi, tt=60000):
    import pandas as pd
    df2_gbmax = dfi.groupby(['e5', 'State'])[['e6']].max() 
    df2_gbmin = dfi.groupby(['e5', 'State'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df_s= dfi.groupby(['e5', 'State'])[['Record Number']].min() 
    df_e= dfi.groupby(['e5', 'State'])[['Record Number']].max() 
    df_y = dfi.groupby(['e5', 'State'])[['cYmm']].mean() 
    df3['Start_frame'] = df_s['Record Number'] 
    df3['End_frame'] =  df_e['Record Number']
    df3['cYmm'] = df_y['cYmm']
    df3 = df3.reset_index()
    df3 = df3[(df3['cYmm'] < 1.9) & (df3['Time']>tt) & (df3['State'].isin(['Stationary Static']))]
    df3['SL_90'] = df3['Start_frame'] -90
    df3['e1'] = df3["End_frame"].shift(1)
    df3['e2'] = df3['e1'] < df3['Start_frame']
    df3 = df3[df3['e2'] ==True]
    SL = df3['SL_90'].tolist()
    EL = df3['End_frame'].tolist()   
    NM = df3['e5'].tolist()
    data = pd.DataFrame()
    for (a, b, c) in zip(SL, EL, NM):
            df = dfi.loc[a:b,].copy()
            df['new_e5'] = c
            data = pd.concat([data, df], ignore_index=True)        

    df3= data.groupby(['new_e5'])[['cYmm']].nth(0)
    df3 = df3.reset_index()

    e5_list = df3['new_e5'].tolist()
    cYmm_list = df3['cYmm'].tolist()
    dt = pd.DataFrame()
    for (a, b) in zip(e5_list, cYmm_list):
        df = data[data['new_e5'] ==a].copy()
        df['Y'] = df['cYmm'] - b
        dt = pd.concat([dt, df], ignore_index=True)
    return dt
        
def cYmm_prerest_long(dfi, pos, tt=60000):
    import pandas as pd
    dfi=dfi.loc[:,["Time_ms","Record Number","State",  "cYmm", "e5", "e6"]]
    df2_gbmax = dfi.groupby(['e5', 'State'])[['e6']].max() 
    df2_gbmin = dfi.groupby(['e5', 'State'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df_s= dfi.groupby(['e5', 'State'])[['Record Number']].min() 
    df_e= dfi.groupby(['e5', 'State'])[['Record Number']].max() 
    df_y = dfi.groupby(['e5', 'State'])[['cYmm']].mean() 
    df3['Start_frame'] = df_s['Record Number'] 
    df3['End_frame'] =  df_e['Record Number']
    df3['cYmm'] = df_y['cYmm']
    df3 = df3.reset_index()
    if pos=='b':
        df3 = df3[(df3['cYmm'] >= 1.9) & (df3['Time']>=tt) & (df3['State'].isin(['Stationary Static']))]
    elif pos=='t':
        df3 = df3[(df3['cYmm'] < 1.9) & (df3['Time']>=tt) & (df3['State'].isin(['Stationary Static']))]
    else:
        raise ValueError("Incorrect keyword use")
    if len(df3)>=1:
        df3['SL_90'] = df3['Start_frame'] -90
        SL = df3['SL_90'].tolist()
        EL = df3['End_frame'].tolist()   
        NM = df3['e5'].tolist()
        data = pd.DataFrame()
        for (a, b, c) in zip(SL, EL, NM):
                df = dfi.loc[a:b,].copy()
                df['new_e5'] = c
                data = pd.concat([data, df], ignore_index=True)  
        df3= data.groupby(['new_e5'])[['cYmm']].nth(0)
        df3 = df3.reset_index()
        e5_list = df3['new_e5'].tolist()
        cYmm_list = df3['cYmm'].tolist()
        dt = pd.DataFrame()
        for (a, b) in zip(e5_list, cYmm_list):
            df = data[data['new_e5'] ==a].copy()
            df['Y'] = df['cYmm'] - b
            dt = pd.concat([dt, df], ignore_index=True)
        return dt
    else:
        raise ValueError("no data")      
        
def cYmm_prerest_short_bottom_selector(dfi):
    import pandas as pd
    df2_gbmax = dfi.groupby(['e5', 'State'])[['e6']].max() 
    df2_gbmin = dfi.groupby(['e5', 'State'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df_s= dfi.groupby(['e5', 'State'])[['Record Number']].min() 
    df_e= dfi.groupby(['e5', 'State'])[['Record Number']].max() 
    df_y = dfi.groupby(['e5', 'State'])[['cYmm']].mean() 
    df3['Start_frame'] = df_s['Record Number'] 
    df3['End_frame'] =  df_e['Record Number']
    df3['cYmm'] = df_y['cYmm']
    df3 = df3.reset_index()
    df3 = df3[(df3['cYmm'] >= 1.9) & (df3['Time']>1000) & (df3['Time']<3000) & (df3['State'].isin(['Stationary Static']))]
    df3['SL_90'] = df3['Start_frame'] -90
    df3['e1'] = df3["End_frame"].shift(1)
    df3['e2'] = df3['e1'] < df3['Start_frame']
    df3 = df3[df3['e2'] ==True]
    df3 = df3.head(1000)
    SL = df3['SL_90'].tolist()
    EL = df3['End_frame'].tolist()   
    NM = df3['e5'].tolist()
    data = pd.DataFrame()
    for (a, b, c) in zip(SL, EL, NM):
            df = dfi.loc[a:b,].copy()
            df['new_e5'] = c
            data = pd.concat([data, df], ignore_index=True)        
    df3= data.groupby(['new_e5'])[['cYmm']].nth(0)
    df3 = df3.reset_index()

    e5_list = df3['new_e5'].tolist()
    cYmm_list = df3['cYmm'].tolist()
    dt = pd.DataFrame()
    for (a, b) in zip(e5_list, cYmm_list):
        df = data[data['new_e5'] ==a].copy()
        df['Y'] = df['cYmm'] - b
        dt = pd.concat([dt, df], ignore_index=True)
    return dt
        
        
def cYmm_prerest_short_top_selector(dfi):
    import pandas as pd
    df2_gbmax = dfi.groupby(['e5', 'State'])[['e6']].max() 
    df2_gbmin = dfi.groupby(['e5', 'State'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df_s= dfi.groupby(['e5', 'State'])[['Record Number']].min() 
    df_e= dfi.groupby(['e5', 'State'])[['Record Number']].max() 
    df_y = dfi.groupby(['e5', 'State'])[['cYmm']].mean() 
    df3['Start_frame'] = df_s['Record Number'] 
    df3['End_frame'] =  df_e['Record Number']
    df3['cYmm'] = df_y['cYmm']
    df3 = df3.reset_index()
    df3 = df3[(df3['cYmm'] < 1.9) & (df3['Time']>1000) & (df3['Time']<3000) & (df3['State'].isin(['Stationary Static']))]
    df3['SL_90'] = df3['Start_frame'] -90
    df3['e1'] = df3["End_frame"].shift(1)
    df3['e2'] = df3['e1'] < df3['Start_frame']
    df3 = df3[df3['e2'] ==True]
    df3 = df3.head(1000)
    SL = df3['SL_90'].tolist()
    EL = df3['End_frame'].tolist()   
    NM = df3['e5'].tolist()
    data = pd.DataFrame()
    for (a, b, c) in zip(SL, EL, NM):
            df = dfi.loc[a:b,].copy()
            df['new_e5'] = c
            data = pd.concat([data, df], ignore_index=True)        

    df3= data.groupby(['new_e5'])[['cYmm']].nth(0)
    df3 = df3.reset_index()

    e5_list = df3['new_e5'].tolist()
    cYmm_list = df3['cYmm'].tolist()
    dt = pd.DataFrame()
    for (a, b) in zip(e5_list, cYmm_list):
        df = data[data['new_e5'] ==a].copy()
        df['Y'] = df['cYmm'] - b
        dt = pd.concat([dt, df], ignore_index=True)
    return dt      

def PreRest_setup(df):
    df['S'] = df['new_bout_duration_rough']/1000
    df['M'] = df['S']/60
    df_b_av1 = df.groupby(['new_bout_frame_number','S', 'M'])[['Y']].mean().reset_index()
    df_b_av1['deltaY'] = df_b_av1['Y'] - (df_b_av1.iloc[0,3])
    df1 = df.groupby(['new_bout_frame_number'])[['Y']].sem().reset_index()
    df_b_av1['YSEM'] = df1['Y']
    df_b_av1['YSEM'] = df_b_av1['YSEM'] -df_b_av1.iloc[0,5]
    data1 = df_b_av1[df_b_av1['S'] < 4]
    return data1






        
def PP_SS_hist_testing(dfi, PP):
    import pandas as pd
    #New df with just the time, state and value for state change
    df2 = dfi.loc[:, ['Time_ms', 'State', 'e5', 'e6', 'Record Number']]
    #Generate the time for each bout of each state, stored in variable df3
    df2_gbmax = df2.groupby(['e5', 'State'])[['e6']].max() 
    df2_gbmin = df2.groupby(['e5', 'State'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3=df3.reset_index()
    df11= df2.groupby(['e5', 'State'])[['Record Number']].min()
    df22=df2.groupby(['e5', 'State'])[['Record Number']].max()
    dfs = df11.reset_index()
    dff=df22.reset_index()
    df3['Start_Frame'] = dfs['Record Number']
    df3['End_Frame'] = dff['Record Number']
    df3_5min = df3[df3['Time'] >= 60000]  #This makes a df with only 1min+ bouts
    lst = df3_5min[df3_5min['State'].isin(['Stationary Static'])] #This makes a df with only the SS occassions from the 1min df
    lst['Pre_Frame'] = lst['Start_Frame'] - 2700
    lst['Post_Frame'] = lst['End_Frame'] + 2700
    
    if PP == 0:
        SL = lst['Pre_Frame'].tolist()
        EL = lst['Start_Frame'].tolist()   
        NM = lst['e5'].tolist()
        data = pd.DataFrame()
        for (a, b, c) in zip(SL, EL, NM):
                df = dfi.iloc[a:b,].copy()
                df['new_e5'] = c
                data = pd.concat([data, df], ignore_index=True)   
        dft = pd.DataFrame(data.groupby('new_e5').cumcount())
        data['Bout_frame_number'] = dft.iloc[:,0]
        data['Bout_duration_rough'] = (data['Bout_frame_number'] * 22.22) + 22
        return data
    elif PP == 1:
        SL = lst['End_Frame'].tolist()
        EL = lst['Post_Frame'].tolist()   
        NM = lst['e5'].tolist()
        data = pd.DataFrame()
        for (a, b, c) in zip(SL, EL, NM):
                df = dfi.iloc[a+1:b,].copy()
                df['new_e5'] = c
                data = pd.concat([data, df], ignore_index=True)   
        dft = pd.DataFrame(data.groupby('new_e5').cumcount())
        data['Bout_frame_number'] = dft.iloc[:,0]
        data['Bout_duration_rough'] = (data['Bout_frame_number'] * 22.22) + 22
        return data
    else:
        raise ValueError('Check Choice of Pre/Post (0 or 1')
    
    
def Timeseries(dfi, tt=0):
    import pandas as pd
    import numpy as np
    end = round(dfi.iloc[-1, 17])
    d = {'Hour': [], 'SSTime': [], 'SATime': [], 'LOTime': []}
    df1_df = pd.DataFrame(data=d)
    a = np.arange(0,end, 0.5)
    b = np.arange(0.5,end+0.5, 0.5)
    
    for (n, m) in zip(a, b):
        df_s = dfi[(dfi.Hour<= m) & (dfi.Hour> n)]
        df2 = df_s.copy()
        df2_gbmax = df2.groupby(['e5', 'State'])[['e6']].max() 
        df2_gbmin = df2.groupby(['e5', 'State'])[['Time_ms']].min()
        df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
        df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
        df3 = df2_gbmax - df2_gbmin
        df3=df3.reset_index()
        df3_ss = df3[df3['State'] == 'Stationary Static']
        df3_sa = df3[df3['State'] == 'Stationary Active']
        df3_lo = df3[df3['State'] == 'Locomotive']
        df3_ss = df3_ss[df3_ss['Time'] > tt]
        c = df3_ss['Time'].sum() / 60000
        d = df3_sa['Time'].sum() / 60000
        e = df3_lo['Time'].sum() / 60000
        df1_df = df1_df.append({'Hour': m, 'SSTime': c, 'SATime': d, 'LOTime': e}, ignore_index=True)
    return df1_df


def DXT(dfi,tt=3000):
    import pandas as pd
    import numpy as np
    
    #X-Tracker Setup 
    df_xtrack_stat = dfi[dfi['State'] != 'Locomotive'].copy()
    df_xtrack_stat['Xtrack']='Stationary'
    df_xtrack_loc = dfi[dfi['State'] == 'Locomotive'].copy()
    df_xtrack_loc['Xtrack']='Locomotive'  
    dfi=pd.concat([df_xtrack_stat,df_xtrack_loc]).sort_index()
    dfi["e7"] = dfi["Xtrack"].shift(1)
    dfi["e8"] = dfi["Xtrack"] != dfi["e7"]
    dfi["e9"] = dfi["e8"].cumsum()
    dfi["e10"] = dfi.Time_ms.shift(-1)   #<-This provides the time from the row below
    
    #DAM setup
    end = round(dfi.Minutes).iloc[-1]
    a = np.arange(0,end, 1)
    b = np.arange(1,end+1, 1)
    cols = ['Time', 'BeamBreak'] #Will need to change the metric names if they change
    lst = []

    for (n, m) in zip(a, b):
        df_1min = dfi[(dfi.Minutes >= n) & (dfi.Minutes < m)]
        if len(df_1min)>1:
            x_min=df_1min["cXmm"].min()
            x_max=df_1min["cXmm"].max()
            if (int(x_min)<31.75) & (int(x_max)>32.25):
                bb = 1
            else:
                bb = 0
            lst.append([m, bb])
        else:
            lst.append([m, 1])
    df1 = pd.DataFrame(lst, columns=cols)
    
    
    df1["e3"] = df1["BeamBreak"].shift(1)
    df1["e4"] = df1["BeamBreak"] != df1["e3"]
    df1["e5"] = df1["e4"].cumsum()
    df1["e6"] = df1.Time.shift(-1) 
    dft = pd.DataFrame(df1.groupby('e5').cumcount())
    df1['Bout_frame_number'] = dft.iloc[:,0]

    df2 = df1[df1['BeamBreak']==0]
    df2 = df2.groupby(['e5']).count().reset_index()
    BoutList = df2[df2['BeamBreak'] >= 5]['e5'].to_list()
    df_DAM = df1.query("e5 in @BoutList").copy()
    df_DAM['Hour'] = df_DAM['Time']/60
    
    #End Dataframe setup
    end = round(dfi.Hour).iloc[-1]
    d = {'Hour': [], 'TruMeLan': [], 'XTracker': [], 'DAM': []}
    df1_df = pd.DataFrame(data=d)
    a = np.arange(0,end, 0.5)
    b = np.arange(0.5,end+0.5, 0.5)
    
    for (n, m) in zip(a, b):
        df2 = dfi[(dfi.Hour<= m) & (dfi.Hour> n)]
        df2_gbmax = df2.groupby(['e5', 'State'])[['e6']].max() 
        df2_gbmin = df2.groupby(['e5', 'State'])[['Time_ms']].min()
        df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
        df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
        df3 = df2_gbmax - df2_gbmin
        df3=df3.reset_index()
        df3_ss = df3[df3['State'] == 'Stationary Static']
        df3_ss = df3_ss[df3_ss['Time'] >= tt]
        c = df3_ss['Time'].sum() / 60000
            
        df2_gbmax = df2.groupby(['e9', 'Xtrack'])[['e10']].max() 
        df2_gbmin = df2.groupby(['e9', 'Xtrack'])[['Time_ms']].min()
        df2_gbmax.rename(columns={'e10':'Time'}, inplace=True)
        df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
        df3 = df2_gbmax - df2_gbmin
        df3=df3.reset_index()
        df3_xt = df3[df3['Xtrack']=='Stationary']
        df3_xt = df3_xt[df3_xt['Time'] >= tt]
        d = df3_xt['Time'].sum() / 60000
        
        df_30min = df_DAM[(df_DAM.Hour > n) & (df_DAM.Hour <= m)]
        e=len(df_30min)
        
        df1_df = df1_df.append({'Hour': m, 'TruMeLan': c, 'XTracker' : d, 'DAM' : e }, ignore_index=True).clip(upper=pd.Series({'Hour': 100, 'TruMeLan': 30, 'XTracker': 30,'DAM': 30}), axis=1)
    return df1_df







def cXmm_rest_selector(dfi, a,b):
    """
    

    Parameters
    ----------
    dfi : dataframe 
        Input dataframe.
    a : int
        The lower bound for SS bout .
    b : int
        The upper bound for SS bout .
    n  : int
        The location you want to record cYmm from
        Default is the final height: -1
        Start height would be: 0

    Returns
    -------
    df : dataframe 
        Output dataframe.

    """
    df2_gbmax = dfi.groupby(['e5', 'State', 'Fly'])[['e6']].max()
    df2_gbmin = dfi.groupby(['e5', 'State', 'Fly'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3['Seconds'] = df3['Time']/1000
    df3['sY'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(0)
    df3['eY'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(-1)
    df3['X'] = dfi.groupby(['e5', 'State'])[['cXmm']].nth(0)
    df=df3.reset_index()
    df = df[df['State'].isin(['Stationary Static'])]
    df = df[(df['Seconds'] > a) & (df['Seconds'] < b)]
    return df

def cXmm_grooming_selector(dfi, a,b):
    """
    

    Parameters
    ----------
    dfi : dataframe 
        Input dataframe.
    a : int
        The lower bound for SS bout .
    b : int
        The upper bound for SS bout .
    n  : int
        The location you want to record cYmm from
        Default is the final height: -1
        Start height would be: 0

    Returns
    -------
    df : dataframe 
        Output dataframe.

    """
    df2_gbmax = dfi.groupby(['e5', 'State', 'Fly'])[['e6']].max()
    df2_gbmin = dfi.groupby(['e5', 'State', 'Fly'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3['Seconds'] = df3['Time']/1000
    df3['sY'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(0)
    df3['eY'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(-1)
    df3['X'] = dfi.groupby(['e5', 'State'])[['cXmm']].nth(0)
    df=df3.reset_index()
    df = df[df['State'].isin(['Stationary Active'])]
    df = df[(df['Seconds'] > a) & (df['Seconds'] < b)]
    return df




def XY_pos_setup(df):
    df['e6'] = df['Fly'].shift(1)
    df['e6'] = df['e6'].fillna(0)
    df["e7"] = ((df["Fly"] > df["e6"]) | ((df["Fly"]==0) & (df["e6"]!=0)))
    df["e8"] = df["e7"].cumsum()
    df['dsY'] =  3.5 - df['sY']
    df['Y_av'] = ((df['sY'] +df['eY'])/2) 
    return df
    
def XY_graph_setup(df1):
    df=df1.copy()
    df['dsY'] =  3.5 - df['sY']
    df=df[df['dsY']>0.5]
    df['Y_av'] = ((df['sY'] +df['eY'])/2)
    return df  


def Ypos_Stationary(dfi, n, day):
    import pandas as pd
    cols = ['Fly','Time of Day','Total Stationary Time', 'Total Bottom Time', 'Total Middle Time', 'Total Ceiling Time', 'Total Bottom Percentage', 
            'Total Middle Percentage', 'Total Ceiling Percentage', 'Long Bottom Bout Count', 'Long Middle Bout Count', 'Long Ceiling Bout Count',
            'Long Bottom Bout Duration', 'Long Middle Bout Duration', 'Long Ceiling Bout Duration', 'Long Bottom Total Duration', 'Long Middle Total Duration', 'Long Ceiling Total Duration',
            'Short Bottom Bout Count', 'Short Middle Bout Count', 'Short Ceiling Bout Count',
            'Short Bottom Bout Duration', 'Short Middle Bout Duration', 'Short Ceiling Bout Duration', 'Short Bottom Total Duration', 'Short Middle Total Duration', 'Short Ceiling Total Duration',
           'SA Bottom Bout Count', 'SA Middle Bout Count', 'SA Ceiling Bout Count',
            'SA Bottom Bout Duration', 'SA Middle Bout Duration', 'SA Ceiling Bout Duration', 'SA Bottom Total Duration', 'SA Middle Total Duration', 'SA Ceiling Total Duration',]
            
    lst = []
    
    if day=='Day':
        TOD='Day'
    elif day=='Night':
        TOD='Night'
    else:
        raise ValueError('Type either "Day" or "Night"')
    #Total 
    df=dfi[dfi['State'] != 'Locomotive']
    total=(len(df)/45)
    dfi_bot =df[df['cYmm'] >=2.4]
    dfi_mid =df[(df['cYmm']<2.4) &(df['cYmm']>1.5)]
    dfi_top =df[df['cYmm'] <=1.5]
    bottom_percentage = ((len(dfi_bot)/45)/total)*100
    middle_percentage = ((len(dfi_mid)/45)/total)*100
    ceiling_percentage = ((len(dfi_top)/45)/total)*100
    
    
    df2_gbmax = dfi.groupby(['e5', 'State', 'Fly'])[['e6']].max()
    df2_gbmin = dfi.groupby(['e5', 'State', 'Fly'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3['Seconds'] = df3['Time']/1000
    df3['sY'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(0)
    df3['eY'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(-1)
    df3['X'] = dfi.groupby(['e5', 'State'])[['cXmm']].nth(0)
    df_all=df3.reset_index()
    
    df = df_all[df_all['State'].isin(['Stationary Static'])].copy()
    #Just Long SS bouts
    df_long = df[(df['Seconds'] >= 60) & (df['Seconds'] < 600000000000000000)].copy()
    df_long['Y_av'] = ((df_long['sY'] +df_long['eY'])/2) 
    long_bot =df_long[df_long['Y_av'] >=2.4]
    long_mid =df_long[(df_long['Y_av']<2.4) &(df_long['Y_av']>1.5)]
    long_top =df_long[df_long['Y_av'] <=1.5]    
    #Just Short SS bouts
    df_short = df[(df['Seconds'] >= 0.5) & (df['Seconds'] < 3)].copy()
    df_short['Y_av'] = ((df_short['sY'] +df_short['eY'])/2) 
    short_bot =df_short[df_short['Y_av'] >=2.4]
    short_mid =df_short[(df_short['Y_av']<2.4) &(df_short['Y_av']>1.5)]
    short_top =df_short[df_short['Y_av'] <=1.5]      
    
    #Just SA bouts
    df = df_all[df_all['State'].isin(['Stationary Active'])].copy()
    df_sa = df[(df['Seconds'] >= 0.5) & (df['Seconds'] < 10000000000)].copy()
    df_sa['Y_av'] = ((df_sa['sY'] +df_sa['eY'])/2) 
    sa_bot =df_sa[df_sa['Y_av'] >=2.4]
    sa_mid =df_sa[(df_sa['Y_av']<2.4) &(df_sa['Y_av']>1.5)]
    sa_top =df_sa[df_sa['Y_av'] <=1.5]      
        
    lst.append([n, TOD, total, len(dfi_bot)/45, len(dfi_mid)/45, len(dfi_top)/45,bottom_percentage,middle_percentage,ceiling_percentage, len(long_bot),len(long_mid),len(long_top),
               long_bot.Seconds.mean(),long_mid.Seconds.mean(),long_top.Seconds.mean(),long_bot.Seconds.sum(),long_mid.Seconds.sum(),long_top.Seconds.sum(),
               len(short_bot),len(short_mid),len(short_top),short_bot.Seconds.mean(),short_mid.Seconds.mean(),short_top.Seconds.mean(),short_bot.Seconds.sum(),short_mid.Seconds.sum(),short_top.Seconds.sum(), 
               len(sa_bot),len(sa_mid),len(sa_top),sa_bot.Seconds.mean(),sa_mid.Seconds.mean(),sa_top.Seconds.mean(),sa_bot.Seconds.sum(),sa_mid.Seconds.sum(),sa_top.Seconds.sum()])
    df1 = pd.DataFrame(lst, columns=cols)
    return df1
    

def Xpos_Stationary(dfi, n, day):
    import pandas as pd
    cols = ['Fly','Time of Day','Total Stationary Time', 'Total Food Time', 'Total Food Near Time', 'Total Middle Left Time', 'Total Middle Right Time', 'Total End Near Time', 'Total End Time', 
           'Total Food Percentage', 'Total Food Near Percentage', 'Total Middle Left Percentage', 'Total Middle Right Percentage', 'Total End Near Percentage', 'Total End Percentage',
           'Long Food Bout Count', 'Long Food Near Bout Count', 'Long Middle Left Bout Count', 'Long Middle Right Bout Count', 'Long End Near Bout Count', 'Long End Bout Count',
          'Long Food Bout Duration', 'Long Food Near Bout Duration', 'Long Middle Left Bout Duration', 'Long Middle Right Bout Duration', 'Long End Near Bout Duration', 'Long End Bout Duration',
            'Long Food Total Duration', 'Long Food Near Total Duration', 'Long Middle Left Total Duration', 'Long Middle Right Total Duration', 'Long End Near Total Duration', 'Long End Total Duration',
            'Short Food Bout Count', 'Short Food Near Bout Count', 'Short Middle Left Bout Count', 'Short Middle Right Bout Count', 'Short End Near Bout Count', 'Short End Bout Count',
          'Short Food Bout Duration', 'Short Food Near Bout Duration', 'Short Middle Left Bout Duration', 'Short Middle Right Bout Duration', 'Short End Near Bout Duration', 'Short End Bout Duration',
            'Short Food Total Duration', 'Short Food Near Total Duration', 'Short Middle Left Total Duration', 'Short Middle Right Total Duration', 'Short End Near Total Duration', 'Short End Total Duration',
             'SA Food Bout Count', 'SA Food Near Bout Count', 'SA Middle Left Bout Count', 'SA Middle Right Bout Count', 'SA End Near Bout Count', 'SA End Bout Count',
          'SA Food Bout Duration', 'SA Food Near Bout Duration', 'SA Middle Left Bout Duration', 'SA Middle Right Bout Duration', 'SA End Near Bout Duration', 'SA End Bout Duration',
            'SA Food Total Duration', 'SA Food Near Total Duration', 'SA Middle Left Total Duration', 'SA Middle Right Total Duration', 'SA End Near Total Duration', 'SA End Total Duration']
            
    lst = []
    
    if day=='Day':
        TOD='Day'
    elif day=='Night':
        TOD='Night'
    else:
        raise ValueError('Type either "Day" or "Night"')
    #Total 
    df=dfi[dfi['State'] != 'Locomotive']
    total=(len(df)/45)
    
    dfi_food =df[(df['cXmm']<14) &(df['cXmm']>=4)]
    dfi_foodnear =df[(df['cXmm']<24) &(df['cXmm']>=14)]
    dfi_middleleft =df[(df['cXmm']<34) &(df['cXmm']>=24)]
    dfi_middleright =df[(df['cXmm']<44) &(df['cXmm']>=34)]
    dfi_endnear =df[(df['cXmm']<54) &(df['cXmm']>=44)]
    dfi_end =df[(df['cXmm']<64) &(df['cXmm']>=54)]
    
    
    df2_gbmax = dfi.groupby(['e5', 'State', 'Fly'])[['e6']].max()
    df2_gbmin = dfi.groupby(['e5', 'State', 'Fly'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3['Seconds'] = df3['Time']/1000
    df3['sY'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(0)
    df3['eY'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(-1)
    df3['X'] = dfi.groupby(['e5', 'State'])[['cXmm']].nth(0)
    df_all=df3.reset_index()
    
    #Just Long SS bouts
    df = df_all[df_all['State'].isin(['Stationary Static'])].copy()
    df_long = df[(df['Seconds'] >= 60) & (df['Seconds'] < 600000000000000000)].copy()
    df_long['Y_av'] = ((df_long['sY'] +df_long['eY'])/2)
    
    long_food =df_long[(df_long['X']<14) &(df_long['X']>=4)]
    long_foodnear =df_long[(df_long['X']<24) &(df_long['X']>=14)]
    long_middleleft =df_long[(df_long['X']<34) &(df_long['X']>=24)]
    long_middleright =df_long[(df_long['X']<44) &(df_long['X']>=34)]
    long_endnear =df_long[(df_long['X']<54) &(df_long['X']>=44)]
    long_end =df_long[(df_long['X']<64) &(df_long['X']>=54)]    
    
    
    #Just Short SS bouts
    df = df_all[df_all['State'].isin(['Stationary Static'])].copy()
    df_short = df[(df['Seconds'] >= 0.5) & (df['Seconds'] < 60)].copy()
    df_short['Y_av'] = ((df_short['sY'] +df_short['eY'])/2) 
    
    short_food =df_short[(df_short['X']<14) &(df_short['X']>=4)]
    short_foodnear =df_short[(df_short['X']<24) &(df_short['X']>=14)]
    short_middleleft =df_short[(df_short['X']<34) &(df_short['X']>=24)]
    short_middleright =df_short[(df_short['X']<44) &(df_short['X']>=34)]
    short_endnear =df_short[(df_short['X']<54) &(df_short['X']>=44)]
    short_end =df_short[(df_short['X']<64) &(df_short['X']>=54)]        
    
    #Just SA bouts
    df = df_all[df_all['State'].isin(['Stationary Active'])].copy()
    df_sa = df[(df['Seconds'] >= 0.5) & (df['Seconds'] < 10000000000)].copy()
    df_sa['Y_av'] = ((df_sa['sY'] +df_sa['eY'])/2) 
    
    sa_food =df_sa[(df_sa['X']<14) &(df_sa['X']>=4)]
    sa_foodnear =df_sa[(df_sa['X']<24) &(df_sa['X']>=14)]
    sa_middleleft =df_sa[(df_sa['X']<34) &(df_sa['X']>=24)]
    sa_middleright =df_sa[(df_sa['X']<44) &(df_sa['X']>=34)]
    sa_endnear =df_sa[(df_sa['X']<54) &(df_sa['X']>=44)]
    sa_end =df_sa[(df_sa['X']<64) &(df_sa['X']>=54)]      
        
    lst.append([n, TOD, total, len(dfi_food)/45, len(dfi_foodnear)/45, len(dfi_middleleft)/45,len(dfi_middleright)/45,len(dfi_endnear)/45,len(dfi_end)/45,
                ((len(dfi_food)/45)/total)*100,((len(dfi_foodnear)/45)/total)*100,((len(dfi_middleleft)/45)/total)*100,((len(dfi_middleright)/45)/total)*100,((len(dfi_endnear)/45)/total)*100,((len(dfi_end)/45)/total)*100,
                len(long_food),len(long_foodnear),len(long_middleleft),len(long_middleright),len(long_endnear),len(long_end),
                long_food.Seconds.mean(),long_foodnear.Seconds.mean(),long_middleleft.Seconds.mean(),long_middleright.Seconds.mean(),long_endnear.Seconds.mean(),long_end.Seconds.mean(),
                long_food.Seconds.sum(),long_foodnear.Seconds.sum(),long_middleleft.Seconds.sum(),long_middleright.Seconds.sum(),long_endnear.Seconds.sum(),long_end.Seconds.sum(),
                len(short_food),len(short_foodnear),len(short_middleleft),len(short_middleright),len(short_endnear),len(short_end),
                short_food.Seconds.mean(),short_foodnear.Seconds.mean(),short_middleleft.Seconds.mean(),short_middleright.Seconds.mean(),short_endnear.Seconds.mean(),short_end.Seconds.mean(),
                short_food.Seconds.sum(),short_foodnear.Seconds.sum(),short_middleleft.Seconds.sum(),short_middleright.Seconds.sum(),short_endnear.Seconds.sum(),short_end.Seconds.sum(),
                len(sa_food),len(sa_foodnear),len(sa_middleleft),len(sa_middleright),len(sa_endnear),len(sa_end),
                sa_food.Seconds.mean(),sa_foodnear.Seconds.mean(),sa_middleleft.Seconds.mean(),sa_middleright.Seconds.mean(),sa_endnear.Seconds.mean(),sa_end.Seconds.mean(),
                sa_food.Seconds.sum(),sa_foodnear.Seconds.sum(),sa_middleleft.Seconds.sum(),sa_middleright.Seconds.sum(),sa_endnear.Seconds.sum(),sa_end.Seconds.sum(),])
                
    df1 = pd.DataFrame(lst, columns=cols)
    return df1
    







def Head_bottom_selector(dfi, tt):
    """
    

    Parameters
    ----------
    dfi : dataframe 
        Input dataframe.
    tt : int
        The SS bout threshold.
    n  : int
        The location you want to record cYmm from
        Default is the final height: -1
        Start height would be: 0

    Returns
    -------
    df : dataframe 
        Output dataframe.

    """
    df2_gbmax = dfi.groupby(['e5', 'State', 'Fly'])[['e6']].max()
    df2_gbmin = dfi.groupby(['e5', 'State', 'Fly'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3['Seconds'] = df3['Time']/1000
    df3['sY'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(0)
    df3['eY'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(-1)
    df3['sH'] = dfi.groupby(['e5', 'State'])[['Heading_deg']].nth(0)
    df3['eH'] = dfi.groupby(['e5', 'State'])[['Heading_deg']].nth(-1)
    df=df3.reset_index()
    df = df[df['State'].isin(['Stationary Static'])]
    df = df[df['Seconds'] > tt]
    df = df[df['eY'] >= 1.9]
    df = df[df['sY'] >= 1.9]
    df['deY'] =  3.5 - df['eY']
    df['dsY'] =  3.5 - df['sY']
    return df

def Head_top_selector(dfi, tt):
    """
    

    Parameters
    ----------
    dfi : dataframe 
        Input dataframe.
    tt : int
        The SS bout threshold.
    n  : int
        The location you want to record cYmm from
        Default is the final height: -1
        Start height would be: 0
    Returns
    -------
    df : dataframe 
        Output dataframe.

    """
    df2_gbmax = dfi.groupby(['e5', 'State', 'Fly'])[['e6']].max()
    df2_gbmin = dfi.groupby(['e5', 'State', 'Fly'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3['Seconds'] = df3['Time']/1000
    df3['sY'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(0)
    df3['eY'] = dfi.groupby(['e5', 'State'])[['cYmm']].nth(-1)
    df3['sH'] = dfi.groupby(['e5', 'State'])[['Heading_deg']].nth(0)
    df3['eH'] = dfi.groupby(['e5', 'State'])[['Heading_deg']].nth(-1)
    df=df3.reset_index()
    df = df[df['State'].isin(['Stationary Static'])]
    df = df[df['Seconds'] > tt]
    df = df[df['eY'] < 1.9]
    df = df[df['sY'] < 1.9]
    df['deY'] = df['eY']
    df['dsY'] = df['sY']
    return df

def Head_adj(dfi):
    import pandas as pd
    dat=dfi
    d1 = dat[(dat['sH'] > 280) & (dat['eH'] > 280)].copy()
    d1['sH'] = d1['sH'] - 360
    d1['eH'] = d1['eH'] - 360
    d2 = dat[(dat['sH'] <= 280) &(dat['eH'] <= 280)].copy()
    d3=dat[(dat['sH'] <= 280) &(dat['eH'] > 280)].copy()
    d4=dat[(dat['sH'] > 280) &(dat['eH'] <= 280)].copy()
    d3_1=d3[d3['sH']< 50].copy()
    d3_2=d3[d3['sH']>= 50].copy()
    d3_1['eH'] = d3_1['eH'] - 360
    d4_1=d4[d4['eH']<50].copy()
    d4_1['sH'] = d4_1['sH'] - 360
    d4_2=d4[d4['eH']>=50].copy()
    data_adj = pd.concat([d1, d2,d3_1, d3_2, d4_1, d4_2], ignore_index=True)
    return data_adj




def Head_300s_bottom_selector(dfi, tt=300000):
    """
    

    Parameters
    ----------
    dfi : dataframe 
        Input dataframe.

    Returns
    -------
    df : dataframe 
        Output dataframe.

    """
    df2_gbmax = dfi.groupby(['e5', 'State'])[['e6']].max() 
    df2_gbmin = dfi.groupby(['e5', 'State'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3=df3.reset_index()
    df3 = df3[df3['Time']>tt]
    df3 = df3[df3['State'].isin(['Stationary Static'])]
    BoutList = df3['e5'].tolist()
    df1 = dfi.loc[:, ['e5', 'cYmm', 'Heading_deg', 'Bout_frame_number', 'Bout_duration_rough', 'Fly']]
    df = df1.query('e5 in @BoutList')
    df = df[df['cYmm'] >= 1.9]
    return df

def Head_300s_top_selector(dfi, tt=300000):
    """
    

    Parameters
    ----------
    dfi : dataframe 
        Input dataframe.

    Returns
    -------
    df : dataframe 
        Output dataframe.

    """
    df2_gbmax = dfi.groupby(['e5', 'State'])[['e6']].max() 
    df2_gbmin = dfi.groupby(['e5', 'State'])[['Time_ms']].min()
    df2_gbmax.rename(columns={'e6':'Time'}, inplace=True)
    df2_gbmin.rename(columns={'Time_ms':'Time'}, inplace=True)
    df3 = df2_gbmax - df2_gbmin
    df3=df3.reset_index()
    df3 = df3[df3['Time']>tt]
    df3 = df3[df3['State'].isin(['Stationary Static'])]
    BoutList = df3['e5'].tolist()
    df1 = dfi.loc[:, ['e5', 'cYmm', 'Heading_deg', 'Bout_frame_number', 'Bout_duration_rough', 'Fly']]
    df = df1.query('e5 in @BoutList')
    df = df[df['cYmm'] < 1.9]
    return df

def Head_dadd(dft):
    import pandas as pd
    from tqdm import tqdm
    df3 = dft.groupby(['e5'])[['Heading_deg']].nth(0).reset_index()
    e5_list = df3['e5'].tolist()
    Head_list = df3['Heading_deg'].tolist()
    data = pd.DataFrame()
    for (a, b) in tqdm(zip(e5_list, Head_list)):
        df = dft[dft['e5'] ==a].copy().reset_index()
        mn = df.Heading_deg.min()
        mx = df.Heading_deg.max()

        if int(mn) <20 & int(mx)>300:
            df_high=df[df['Heading_deg']>250]
            df_low= df[df['Heading_deg']<100]
            df_low['Heading_deg'] = df_low['Heading_deg'] + 360 
            df = pd.concat([df_high, df_low], ignore_index=False)
            df['H'] = df['Heading_deg'] - df.loc[0,'Heading_deg']
        else:
            df['H'] = df['Heading_deg'] - b
        data = pd.concat([data, df], ignore_index=True)
    return data

