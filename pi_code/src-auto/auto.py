import RPi.GPIO as gpio
import time
import zerorpc
import cv2
import tensorflow as tf
import numpy as np

# Constants
MIN_SPEED = 6
MED_SPEED = 16
MAX_SPEED = 23
CROP_AMOUNT = 30
CAPTURE_TIME = 0.13

# GPIO pins
in1 = 37
in2 = 36
in3 = 38
in4 = 40
enA = 35
enB = 32
pwmA = 0
pwmB = 0

# Variables
leftSpeed = 0
rightSpeed = 0

# Webcam setup
cam = cv2.VideoCapture(0)
cam.set(3, 160)
cam.set(4, 120)
if cam.isOpened():
  ret = True
else:
  ret = False
print("Webcam is set up")

# Load model
model = tf.keras.models.load_model('direction_calculator.model')
print("Model loaded")

class Control(object):

    def forward(self):
        print("FORWARD")
        global pwmA, pwmB
        straight()
        pwmA.ChangeDutyCycle(leftSpeed)
        pwmB.ChangeDutyCycle(rightSpeed)
        time.sleep(2)
        stop()
        pass

    def backward(self):
        print("BACKWARD")
        global pwmA, pwmB
        reverse()
        pwmA.ChangeDutyCycle(leftSpeed)
        pwmB.ChangeDutyCycle(rightSpeed)
        time.sleep(2)
        stop()
        pass

    def auto(self, duration):
        print("AUTO")
        sec = 0
        while sec < duration:
            setDirection()
            sec += CAPTURE_TIME
        stop()
        pass

    def cleanup(self):
        global pwmA, pwmB
        pwmA.stop()
        pwmB.stop()
        gpio.cleanup()
        exit()
        pass


def init():
    global pwmA, pwmB, enA, enB
    gpio.setmode(gpio.BOARD)
    gpio.setup(in1, gpio.OUT)
    gpio.setup(in2, gpio.OUT)
    gpio.setup(in3, gpio.OUT)
    gpio.setup(in4, gpio.OUT)
    gpio.setup(enA, gpio.OUT)
    gpio.setup(enB, gpio.OUT)
    pwmA = gpio.PWM(enA, 100)
    pwmB = gpio.PWM(enB, 100)
    pwmA.start(0)
    pwmB.start(0)
    print("INITIALIZED")

def straight():
    global leftSpeed, rightSpeed
    leftSpeed = MED_SPEED
    rightSpeed = MED_SPEED
    gpio.output(in1, False)
    gpio.output(in2, True)
    gpio.output(in3, False)
    gpio.output(in4, True)

def reverse():
    global leftSpeed, rightSpeed
    leftSpeed = MED_SPEED
    rightSpeed = MED_SPEED
    gpio.output(in1, True)
    gpio.output(in2, False)
    gpio.output(in3, True)
    gpio.output(in4, False)

def left():
    global leftSpeed, rightSpeed
    leftSpeed = MIN_SPEED
    rightSpeed = MAX_SPEED
    gpio.output(in1, True)
    gpio.output(in2, False)
    gpio.output(in3, False)
    gpio.output(in4, True)

def right():
    global leftSpeed, rightSpeed
    leftSpeed = MAX_SPEED
    rightSpeed = MIN_SPEED
    gpio.output(in1, False)
    gpio.output(in2, True)
    gpio.output(in3, True)
    gpio.output(in4, False)

def stop():
    global pwmA, pwmB
    gpio.output(in1, False)
    gpio.output(in2, False)
    gpio.output(in3, False)
    gpio.output(in4, False)
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)
    print("STOP")


# Use AI to calculate next direction
def setDirection():
    global ret, leftSpeed, rightSpeed, model
    if (ret):
        # Take picture
        ret, frame = cam.read()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Crop image
        img = img[CROP_AMOUNT:img.shape[0], 0:img.shape[1]]
        # Format ndarray
        img = np.expand_dims(img, axis=0)
        # Get prediction
        direction = int(np.argmax(model.predict(img)))
        if direction == 0:
            left()
        elif direction == 2:
            right()
        else:
            straight()
    # Update
    pwmA.ChangeDutyCycle(leftSpeed)
    pwmB.ChangeDutyCycle(rightSpeed)


# The following code executes on load
init()

server = zerorpc.Server(Control())
server.bind("tcp://127.0.0.1:4242")
server.run()
