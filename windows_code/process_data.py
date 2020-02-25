import numpy as np
import cv2
import os

SAMPLE_IMG_INDEX = 20

# -- READ CONSTANTS FROM 'constants.txt' --
constants_file = open("constants.txt", "r")
file_lines = constants_file.readlines()
get_scale, get_crop, get_delay = False, False, False
IMG_SCALE, CROP_AMOUNT, FRAME_DELAY = -1, -1, -1
for line in file_lines:
    if line == "image scale:\n":
        get_scale = True
    elif line == "image crop amount:\n":
        get_crop = True
    elif line == "frame delay:\n":
        get_delay = True
    elif get_scale == True:
        IMG_SCALE = int(line)
        get_scale = False
    elif get_crop == True:
        CROP_AMOUNT = int(line)
        get_crop = False
    elif get_delay == True:
        FRAME_DELAY = int(line)
        get_delay = False

# -- FUNCTIONS --
def resizeImage(list, index):
    return cv2.resize(list[index], None, fx=IMG_SCALE, fy=IMG_SCALE)

# Make sure that we have required raw data
if not os.path.isfile("raw_data\\y.txt"):
    print("\nError! y.txt not found\n")
    exit(1)

# Clear 'processed_data' folder
os.system("del processed_data")

# Load text data
file = open("raw_data\\y.txt", "r")
y = np.loadtxt(file, dtype=int)
data_length = y.shape[0]
print("Data length: " + str(data_length))

# Set image width and height variables
img = cv2.imread("raw_data\\" + str(SAMPLE_IMG_INDEX) + ".png")
img_width = img.shape[1]
img_height = img.shape[0]

# Load all images
x = np.zeros((data_length, img_height, img_width))
for i in range(data_length):
    x[i] = cv2.imread("raw_data\\" + str(i) + ".png", cv2.IMREAD_GRAYIMG_SCALE)

# Set dtype
x = x.astype(np.uint8)

# Crop images
uncropped = np.copy(x)
x = x[0:data_length, CROP_AMOUNT:img_height, 0:img_width]
print("Crop percent: " + str(CROP_AMOUNT/img_height*100) + "%")
print("New size: " + str(x[SAMPLE_IMG_INDEX].shape))

# Go through images one by one
saved_indices = []
finish = False
index = 0
image_to_show = resizeImage(x, index)
while not finish:
    if not os.path.isfile("raw_data\\"+str(index)+".png"):
        print("File '"+str(index)+".png' does not exist")
    elif index in saved_indices:
        print("Image #" + str(index) + " is saved")
    else:
        print("Image #" + str(index) + " is NOT saved")
    print("Direction: " + str(y[index-FRAME_DELAY]))

    cv2.imshow("image", image_to_show)
    key = cv2.waitKey(0)

    # Previous image
    if key == ord('a') and index >= 1:
        index -= 1
        image_to_show = resizeImage(x, index)
    # Next image
    elif key == ord('d') and index < data_length - 1:
        index += 1
        image_to_show = resizeImage(x, index)
        if index == data_length - 1:
            print("end of data")
    # Save image and go to next if possible
    elif key == ord('s'):
        if os.path.isfile("raw_data\\"+str(index)+".png") and not index in saved_indices:
            cv2.imwrite("processed_data\\"+str(len(saved_indices))+".png", x[index])
            saved_indices.append(index)
        if index < data_length - 1:
            index += 1
            image_to_show = resizeImage(x, index)
        if index == data_length - 1:
            print("end of data")
    # Undo previous save
    elif key == ord('w'):
        file = "processed_data\\"+str(len(saved_indices)-1)+".png"
        if os.path.isfile(file):
            os.system("del " + file)
            del saved_indices[-1]
    # Edit direction
    elif key == ord('e'):
        editing = True
        while editing:
            key = cv2.waitKey(0)
            editing = False
            if key == ord('q'):
                y[index-FRAME_DELAY] = 0
            elif key == ord('w'):
                y[index-FRAME_DELAY] = 1
            elif key == ord('e'):
                y[index-FRAME_DELAY] = 2
            else:
                editing = True
    # Show cropped
    elif key == ord('c'):
        cv2.imshow("image", resizeImage(uncropped, index))
        while cv2.waitKey(0) != ord('c'):
            continue
    # Exit with ESC button
    elif key == 27:
        finish = True

print(saved_indices)

file = open("processed_data\\y.txt", "w+")
for index in saved_indices:
    file.write(str(y[index-FRAME_DELAY]) + "\n")

file.close()
print("Saving complete!")
