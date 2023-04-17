import os
for i in range(len(os.listdir("."))):
    file_path = os.path.join(".\\", os.listdir(".")[i])
    os.rename(file_path, str(i) + ".mp4")

