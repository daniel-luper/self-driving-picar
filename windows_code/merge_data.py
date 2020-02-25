import os
import numpy as np

# Ask user which folder we want to merge with
print("Merge 'processed_data' with: ")
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

# Load 'processed_file\y.txt'
processed_file = open("processed_data\\y.txt", "r")
directions = np.loadtxt(processed_file, dtype=int)
processed_length = directions.shape[0]
processed_file.close()


# Create file if it doesn't exist yet
if not os.path.isfile(path + "y.txt"):
    os.system("type nul > " + path + "y.txt")

# Find next index that hasn't been used in 'final's' contents
# This is the index at which our incoming data should start
final_file = open(path + "y.txt", "r")
start_index = np.loadtxt(final_file).shape[0]

# Append text from 'processed_data' to our final text file
final_file = open(path + "y.txt", "a")
for direction in directions:
    final_file.write(str(direction) + "\n")
final_file.close()

# Copy images over to our final folder
for i in range(0, processed_length):
    os.system("copy processed_data\\"+str(i)+".png "+path+str(i + start_index)+".png")