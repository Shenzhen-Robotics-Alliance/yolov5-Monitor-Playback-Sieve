import os
for i in range(len(os.listdir(".\\data\\videos\\"))):
    if os.listdir(".\\data\\videos\\")[i].split(".")[-1] != "mp4": # if the suffix name of the file is not mp4
        continue # leave it alone
    file_path = os.path.join(".\\", os.listdir(".")[i])
    os.rename(file_path, str(i) + ".mp4") # rename all the videos so for easier sorting

