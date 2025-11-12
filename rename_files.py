import os
import glob

# Directory containing the CSV files
directory = r"D:\ACC Lab Dropbox\ACC Lab\Nicole Lee\eOPN3 manuscript\Data\TruMelan\Jonny\eOPN3 PIEZO\Piezo x eOPN3_Green_1s"

print(f"Working in directory: {directory}")
print(f"Directory exists: {os.path.exists(directory)}")

# Find all CSV files containing "m4xPiezo Green"
pattern = os.path.join(directory, "*m4xPiezo Green*.csv")
files = glob.glob(pattern)

print(f"Found {len(files)} files to rename:")

# Rename each file
for old_path in files:
    # Get the filename without the full path
    old_filename = os.path.basename(old_path)
    
    # Create new filename: replace "m4xPiezo Green" with "Piezo x eOPN3_1s"
    new_filename = old_filename.replace("m4xPiezo Green", "Piezo x eOPN3_1s")
    
    # Create the new full path
    new_path = os.path.join(directory, new_filename)
    
    try:
        # Rename the file
        os.rename(old_path, new_path)
        print(f"SUCCESS: Renamed {old_filename} -> {new_filename}")
    except Exception as e:
        print(f"ERROR: Could not rename {old_filename}: {e}")

print("Renaming complete!")