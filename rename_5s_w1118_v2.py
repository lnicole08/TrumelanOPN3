import os
import re

folder_path = r'C:\Users\User\ACC Lab Dropbox\ACC Lab\Nicole Lee\eOPN3 manuscript\Data\TruMelan\Reformatted\w1118 x elav_ATR'

# List all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv') and '_5s_' not in f]

print(f'Found {len(csv_files)} CSV files still needing _5s')
print('\nExample transformations:')

# Show first few examples
for i, file in enumerate(csv_files[:3]):
    # Handle both patterns: _ATR_2_ and _ATR_
    if '_ATR_2_' in file:
        new_name = file.replace('_ATR_2_', '_ATR_5s_2_')
    elif '_ATR_' in file:
        new_name = re.sub(r'(.*elav_ATR)_(\d+\.csv)', r'\1_5s_\2', file)
    else:
        new_name = file  # No change
    
    print(f'  {file}')
    print(f'  -> {new_name}')

# Rename all files
renamed_count = 0
for file in csv_files:
    old_path = os.path.join(folder_path, file)
    
    # Handle both patterns: _ATR_2_ and _ATR_
    if '_ATR_2_' in file:
        new_name = file.replace('_ATR_2_', '_ATR_5s_2_')
    elif '_ATR_' in file:
        new_name = re.sub(r'(.*elav_ATR)_(\d+\.csv)', r'\1_5s_\2', file)
    else:
        continue  # Skip files that don't match pattern
    
    new_path = os.path.join(folder_path, new_name)
    
    if old_path != new_path:
        os.rename(old_path, new_path)
        renamed_count += 1

print(f'\nSuccessfully renamed {renamed_count} files')

# Verify the renaming
print('\nVerifying - all files now have _5s:')
all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
with_5s = [f for f in all_files if '_5s' in f]
print(f'  Total CSV files: {len(all_files)}')
print(f'  Files with _5s: {len(with_5s)}')
print('\nFirst 3 examples:')
for f in sorted(with_5s)[:3]:
    print(f'  {f}')