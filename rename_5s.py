import os
import re

folder_path = r'C:\Users\User\ACC Lab Dropbox\ACC Lab\Nicole Lee\eOPN3 manuscript\Data\TruMelan\Reformatted\elav x eOPN3_ATR'

# List all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

print(f'Found {len(csv_files)} CSV files to rename')
print('\nExample transformations:')

# Show first few examples
for i, file in enumerate(csv_files[:3]):
    # Pattern: everything up to _ATR, then underscore and number
    new_name = re.sub(r'(.*eOPN3_ATR)_(\d+\.csv)', r'\1_5s_\2', file)
    print(f'  {file}')
    print(f'  -> {new_name}')

# Rename all files
renamed_count = 0
for file in csv_files:
    old_path = os.path.join(folder_path, file)
    new_name = re.sub(r'(.*eOPN3_ATR)_(\d+\.csv)', r'\1_5s_\2', file)
    new_path = os.path.join(folder_path, new_name)
    
    if old_path != new_path:
        os.rename(old_path, new_path)
        renamed_count += 1

print(f'\nSuccessfully renamed {renamed_count} files')

# Verify the renaming
print('\nVerifying - first 3 files after renaming:')
new_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.csv')])[:3]
for f in new_files:
    print(f'  {f}')