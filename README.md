# yolov5-Monitor-Playback-Sieve
***
A simple monitor playback watcher based on yolov5s.pt model that separates the time interval whenever someone enters a selected region


## What does it do?

The yolov5-Monitor-Playback-Sieve aims to reduce the work of humans when trying to watch a monitor-playback 

It watches the videos for you and marks the time intervals whenever anyone enters a region that you set

## Requirements
This program relies on yolov5s image detection model
To install the requirements for yolov5, just run:

        pip install -r requirements.txt  # install

Yolo will download the pretrained model automatically from the internet

For further instructions like installing cuda-based pytorch, see [README.yolov5.md](README.yolov5.md)

## Running
Put the videos into .\data\images\ in the form of mp4
Firstly, you need to detect a video using yolov5, and export the data into a txt file

        python ".\rename videos.py" # rename the videos (optinal)
        python .\detect.py --save-txt --weights yolov5s --source .\data\images\[file-name].mp4 # run the detection on the selected video

Next, run the program that processes the data that yolo has just exported

        python ".\process yolo result.py"

You will need to provide the following information according to guidance of the program:

1. the frame rate that your video is recorded
2. the place where yolov5 exported its data, just see the folder .\runs\detect\ and look for the latest exporting directory, it is the form of exp, exp1, exp2 and so on
3. the region that you need to keep track on, in the format of:
    - the x-coordinate of the center of your region, from left to right and from 0~1, as float numbers
    - the y-coordinate of the center of your region, from top to bottom and from 0~1, as float numbers
    - the width of your selected region, from 0~1, where 1 is the width of the whole view
    - the height of your selected region, from 0~1, where is the height of the whole view
    
    For example, if you need to detect the center 60% region of the screen, just go (0.5, 0.5, 0.6, 0.6); if you need id to keep an eye on the left half of the view, go (0.75, 0.5, 0.5, 1)