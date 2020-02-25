## save data but no ultrasound
##
import RPi.GPIO as gpio
import time
import zerorpc
import cv2
import threading
import os

# Constants
SAVE_FREQUENCY = 0.25
CAM_WIDTH = 160
CAM_HEIGHT = 120

# GPIO pins
in1 = 37
in2 = 36
in3 = 38
in4 = 40
enA = 35
enB = 32

# Direction that the car is going in
# 0 for left, 1 for straight, 2 for right
direction = 0
pwmA = 0
pwmB = 0
leftSpeed = 0
rightSpeed = 0

# Webcam setup
cam = cv2.VideoCapture(0)
cam.set(3, CAM_WIDTH)
cam.set(4, CAM_HEIGHT)
if cam.isOpened():
  ret = True
else:
  ret = False
print("Webcam is set up")

# Save data setup
file = open("../data/temp.txt", "w")
count = 0
print("Save data is set up")


class Control(object):
    def move(self, lSpeed, rSpeed):
        # Update speed
        global leftSpeed, rightSpeed
        leftSpeed = lSpeed
        rightSpeed = rSpeed
        pass

    def forward(self):
        global direction
        direction = 1
        pass

    def backward(self):
        global direction
        direction = -1
        pass

    def left(self):
        global direction
        direction = 0
        pass

    def right(self):
        global direction
        direction = 2
        pass

    def gpio_stop(self):
        gpio.output(in1, False)
        gpio.output(in2, False)
        gpio.output(in3, False)
        gpio.output(in4, False)
        print("STOPPED")
        pass

    def cleanup(self):
        global timer, file, pwmA, pwmB
        pwmA.stop()
        pwmB.stop()
        timer.cancel()
        file.close()
        os.system("cp ../data/temp.txt ../data/y.txt")
        gpio.cleanup()
        pass

    def shutdown(self):
        os.system("sudo shutdown now -h")

def init():
  global pwmA, pwmB
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
  pass

def go_forward():
  gpio.output(in1, False)
  gpio.output(in2, True)
  gpio.output(in3, False)
  gpio.output(in4, True)
  pass

def go_backward():
  gpio.output(in1, True)
  gpio.output(in2, False)
  gpio.output(in3, True)
  gpio.output(in4, False)
  pass

def go_left():
  gpio.output(in1, True)
  gpio.output(in2, False)
  gpio.output(in3, False)
  gpio.output(in4, True)
  pass

def go_right():
  gpio.output(in1, False)
  gpio.output(in2, True)
  gpio.output(in3, True)
  gpio.output(in4, False)
  pass


# So that we can run other functions in background
def set_interval(func, sec):
  def func_wrapper():
    set_interval(func, sec)
    func()
  t = threading.Timer(sec, func_wrapper)
  t.start()
  return t

# Save data
def save_data():
  global ret, count, direction, file, pwmA, pwmB, leftSpeed, rightSpeed
  if (ret):
    ret, frame = cam.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("../data/" + str(count) + ".png", img)
  try:
    file.write(str(direction) + "\n")
  except IOError:
    exit()
  if (direction == 0):
    go_left()
  elif (direction == 1):
    go_forward()
  elif (direction == 2):
    go_right()
  elif (direction == -1):
    go_backward()
  pwmA.ChangeDutyCycle(leftSpeed)
  pwmB.ChangeDutyCycle(rightSpeed)
  print("Count: " + str(count))
  print("Direction: " + str(direction) + "\n")
  count = count + 1


init()

timer = set_interval(save_data, SAVE_FREQUENCY)

server = zerorpc.Server(Control())
server.bind("tcp://127.0.0.1:4242")
server.run()
