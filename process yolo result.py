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
data_dir = ".\\runs\\detect\\" + input("the name of the exported data? (usually exp1,exp2 and so on)") + "\\labels\\"
obj_type_for_human = 0
frame_rate = 50

exported_data_files = os.listdir(data_dir)

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

for data_id in range(len(exported_data_files)):
    data_path = os.path.join(data_dir, exported_data_files[data_id])
    frame_id = exported_data_files[data_id].split("_")[1]
    flag = False

    with open(data_path, mode="r") as frame_data:
        objects = frame_data.read().splitlines()
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
            if ( not ( # whenever the two matrix are NOT apart from each other, they intersects
                obj_rect[1][0] < targeted_sector[0][0] or # the right side of the object is on the left of the left side of the targeted area
                obj_rect[0][0] > targeted_sector[1][0] or # the left side of the object is on the right of the right side of the targeted area
                obj_rect[1][1] < targeted_sector[0][1] or # the upper side of the object is below the bottom of the targeted area
                obj_rect[0][1] > targeted_sector[0][1] # the bottom of the object is on top of the upper side of the targeted area
            )):
                flag = True

    if flag:
        sys.stdout.write("processing data from file: " + data_path + ", frame (" +str(data_id) + "/" + str(len(exported_data_files)) + ")  found targets in this frame")
        sys.stdout.write("\r")
        sys.stdout.flush()
        marked_frames.append(data_id)
    else:
        sys.stdout.write("processing data from file: " + data_path + ", frame (" + str(data_id) + "/" + str(len(exported_data_files)) + ")  no targets in the selected sector")
        sys.stdout.write("\r")
        sys.stdout.flush()


print("<-- finished! marked", len(marked_frames), "frames in total -->")


# using all the frames that have just been marked, highlight the period of videos
marked_frames.sort()

marked_periods = []
for i in marked_frames:
    frame_time = i / frame_rate # the time at which this frame comes up
    try:
        prev_period = marked_periods[-1] # the last time when a frame is marked
        if frame_time - prev_period[1] <= 5: # if two frames are within 5 seconds close to each other
            marked_periods[-1] = (marked_periods[0] , frame_time+5) # just lengthen the last period, in other word, connect the present period with the last one
            continue
    except IndexError:
        pass

    marked_periods.append((frame_time-5, frame_time+5))

print(marked_periods)