import os

directory = r"D:\ACC Lab Dropbox\ACC Lab\Nicole Lee\eOPN3 manuscript\Data\TruMelan\Leif data\w1118_nsyb_csv"

print(f"Directory exists: {os.path.exists(directory)}")

if os.path.exists(directory):
    files = os.listdir(directory)
    print(f"Number of files: {len(files)}")
    for i, file in enumerate(files[:10]):  # Show first 10 files
        print(f"{i+1}. {file}")
else:
    print("Directory not found")