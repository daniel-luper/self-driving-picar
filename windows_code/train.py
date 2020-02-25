import tensorflow as tf
import numpy as np
import cv2

SAMPLE_IMG_INDEX = 20

# Load training text data
file_train = open("train_data\\y.txt", "r")
y_train = np.loadtxt(file_train)
train_length = y_train.shape[0]

# Load testing text data
file_test = open("test_data\\y.txt", "r")
y_test = np.loadtxt(file_test)
test_length = y_test.shape[0]

# Set image width and height variables
img = cv2.imread("train_data\\" + str(SAMPLE_IMG_INDEX) + ".png")
img_width = img.shape[1]
img_height = img.shape[0]

# Load all images
x_train = np.zeros((train_length, img_height, img_width))
for i in range(train_length):
    x_train[i] = cv2.imread("train_data\\" + str(i) + ".png", cv2.IMREAD_GRAYSCALE)
x_test = np.zeros((test_length, img_height, img_width))
for i in range(test_length):
    x_test[i] = cv2.imread("test_data\\" + str(i) + ".png", cv2.IMREAD_GRAYSCALE)

# Set dtype
x_train = x_train.astype(np.uint8)
x_test = x_test.astype(np.uint8)

# Normalize
x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)


# ..............
# ...Training...
# ..............
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape = (img_height, img_width)),
    tf.keras.layers.Dense(512, activation=tf.nn.relu),
    tf.keras.layers.Dense(512, activation=tf.nn.relu),
    tf.keras.layers.Dense(128, activation=tf.nn.relu),
    tf.keras.layers.Dense(3, activation=tf.nn.softmax)
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=8)

val_loss, val_acc = model.evaluate(x_test, y_test)
print(val_loss, val_acc)

model.save("my_neural_network.model")

#### NOTES: #################################################
# With the default 20,000 image dataset and these settings, #
# I obtained an accuracy of 76%.                            #
#                                                           #
# 76% might seem low, but it's ok because the neural        #
# network only needs to accurately determine the direction  #
# of sharp turns. When the car is supposed to go more or    #
# less straight, any direction (left, right, or straight)   #
# is permissible.                                           #
#############################################################