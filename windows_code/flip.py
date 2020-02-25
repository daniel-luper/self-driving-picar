import os
import cv2
import numpy as np

# -- READ CONSTANTS FROM 'constants.txt' --
constants_file = open("constants.txt", "r")
file_lines = constants_file.readlines()
get_width, get_height = False, False
IMG_WIDTH, IMG_HEIGHT = -1, -1
for line in file_lines:
    if line == "image width:\n":
        get_width = True
    elif line == "image height:\n":
        get_height = True
    elif get_width == True:
        IMG_WIDTH = int(line)
        get_width = False
    elif get_height == True:
        IMG_HEIGHT = int(line)
        get_height = False

# Ask user which dataset we want to flip
print("Flip data in: ")
print("  1. 'train_data'")
print("  2. 'test_data'")
while True:
    val = input("Enter '1' or '2': ")
    if val == "1":
        path = "train_data\\"
        break
    elif val == "2":
        path = "test_data\\"
        break
    else:
        print("Invalid input\n")

# Load directions
file = open(path + "y.txt", "r")
directions = np.loadtxt(file, dtype=int)
length = directions.shape[0]
file.close()

# Load images
images = np.zeros((length, IMG_HEIGHT, IMG_WIDTH))
for i in range(length):
    images[i] = cv2.imread(path + str(i) + ".png", cv2.IMREAD_GRAYSCALE)

# Set dtype
images = images.astype(np.uint8)

# Flip!
images = np.flip(images, 2)
for i in range(length):
    if directions[i] == 0:
        directions[i] = 2
    elif directions[i] == 2:
        directions[i] = 0

# Save
for i in range(length):
    cv2.imwrite(path + str(length + i)+".png", images[i])
file = open(path + "y.txt", "a")
for direction in directions:
    file.write(str(direction) + "\n")
file.close()