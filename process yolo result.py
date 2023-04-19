"""
find all the humans inside the view of the camera who entered a set sector
using the data exported from yolo5

when two matrices are in a 2d-plane, you can determine whether the two will intersect by looking at the four corners of one matrix and see if they lies inside the other,
if one them lies inside the other matrix, or the other way around, the two matrix will absolutely intersect with each other

yolov5 txt data sample: label_index, cx, cy, w, h
label_index: the id of the label, 0 for humans
cx: the x coordinate of the center of the rectangle that the object sits in, ranged from 0-1, where 1 is the width of the whole picture, and from LEFT to RIGHT
cy: the y coordinate of the center of the rectangle that the object sits in, ranged from 0-1, where 1 is the height of the whole picture, and from UP to DOWN
w: the width of the rectangle that an object sits in, ranged from 0-1 where 1 is the width of the whole picture
h: the height of the rectangle that an object sits in, ranged from 0-1 where 1 is the height of the whole picture
"""
import os, sys
# the path to the saved data
data_file = ".\\runs\\detect\\" + input("the name of the exported data? (usually exp1,exp2 and so on)") + "\\labels\\"
# open the single file
data_file += os.listdir(data_file)[0]

obj_type_for_human = 0
frame_rate = 5
extend_length = 5 # the amount of seconds to extend from the frames that are marked

'''targeted_sector = [
    [
        float(input("the x-coordinate of the left-up corner of the sector? (float 0~1, from left to right)")),
        float(input("the y-coordinate of the left-up corner of the sector? (float 0~1, from up to down")),
    ],
    [
        float(input("the x-coordinate of the right-bottom corner of the sector? (float 0~1, from left to right")),
        float(input("the y-coordinate of the right-bottom corner of the sector? (float 0~1, from up to down"))
    ]
]'''

targeted_sector_center = [
    float(input("the x-coordinate of the center of the sector? (float 0~1, from left to right)")),
    float(input("the y-coordinate of the center of the sector? (float 0~1, from up to down")),
]

targeted_sector_size = [
    float(input("the width of the sector?")),
    float(input("the height of the sector?"))
]

targeted_sector = [
    [
        targeted_sector_center[0] - targeted_sector_size[0]/2, # the x-coordinate of the left-up corner of the sector
        targeted_sector_center[1] - targeted_sector_size[1]/2  # the y-coordinate of the left-up corner of the sector
    ],
    [
        targeted_sector_center[0] + targeted_sector_size[0] / 2, # the x-coordinate of the right-bottom corner of the sector
        targeted_sector_center[1] + targeted_sector_size[1] / 2  # the y-coordinate of the right-bottom corner of the sector
    ]
]


marked_frames = []
with open(data_file, mode="r") as frames_data_file: # open the single-file data
    frames_data = frames_data_file.read().split("/") # load the data and split the frames
    print("<--successfully loaded", len(frames_data), "frames from file", data_file, "-->")
    for frame_id in range(len(frames_data)):
        flag = False
        frame_data = frames_data[frame_id] # the data for this single frame

        objects = frame_data.splitlines()
        for obj in objects:
            obj_type = float(obj.split()[0])
            obj_pos = [float(obj.split()[1]), float(obj.split()[2])]
            obj_size = [float(obj.split()[3]), float(obj.split()[4])]

            obj_rect = [
                [
                    obj_pos[0] - (obj_size[0] / 2), # x coordinate of the left-up corner
                    obj_pos[1] - (obj_size[1] / 2), # y coordinate of the left-up corner
                ],
                [
                    obj_pos[0] + (obj_size[0] / 2),  # x coordinate of the right-bottom corner
                    obj_pos[1] + (obj_size[1] / 2),  # y coordinate of the right-bottom corner
                ]
            ]

            if obj_type != obj_type_for_human:
                continue
            #print(obj_rect, targeted_sector)

            if ( not ( # whenever the two matrix are NOT apart from each other, they intersects
                obj_rect[1][0] < targeted_sector[0][0] or # the right side of the object is on the left of the left side of the targeted area
                obj_rect[0][0] > targeted_sector[1][0] or # the left side of the object is on the right of the right side of the targeted area
                obj_rect[1][1] < targeted_sector[0][1] or # the upper side of the object is below the bottom of the targeted area
                obj_rect[0][1] > targeted_sector[1][1] # the bottom of the object is on top of the upper side of the targeted area
            )):
                flag = True

        if flag:
            sys.stdout.write("processing data from frame (" +str(frame_id) + "/" + str(len(frames_data)) + ")  found targets in this frame")
            sys.stdout.write("\r")
            sys.stdout.flush()
            marked_frames.append(frame_id)
        else:
            sys.stdout.write("processing data from frame (" +str(frame_id) + "/" + str(len(frames_data)) + ")  no targets in the selected sector")
            sys.stdout.write("\r")
            sys.stdout.flush()

sys.stdout.flush()
print()
print("<-- finished! marked", len(marked_frames), "frames in total -->")


# using all the frames that have just been marked, highlight the period of videos
marked_frames.sort()

marked_periods = []
for i in marked_frames:
    frame_time = i / frame_rate # the time at which this frame comes up
    if marked_periods: # if there are periods that have already been marked
        prev_period = marked_periods[-1] # the last time when a frame is marked
        if frame_time - prev_period[1] <= 5: # if two frames are within 5 seconds close to each other
            marked_periods[-1] = (marked_periods[-1][0] , min(frame_time+extend_length, len(frames_data) / frame_rate)) # just lengthen the last period, in other word, connect the present period with the last one
            continue

    marked_periods.append((max(frame_time-extend_length, 0), min(frame_time+extend_length, len(frames_data) / frame_rate)))

print(marked_periods)