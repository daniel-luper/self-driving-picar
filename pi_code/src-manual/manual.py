import RPi.GPIO as gpio
import time
import zerorpc
import os

# GPIO pins
in1 = 37
in2 = 36
in3 = 38
in4 = 40
enA = 35
enB = 32
trig = 15
echo = 16

class Control(object):

    def init(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(in1, gpio.OUT)
        gpio.setup(in2, gpio.OUT)
        gpio.setup(in3, gpio.OUT)
        gpio.setup(in4, gpio.OUT)
        gpio.setup(enA, gpio.OUT)
        gpio.setup(enB, gpio.OUT)
        gpio.setup(trig, gpio.OUT)
        gpio.setup(echo, gpio.IN)
        gpio.output(trig, False)
        self.pwmA = gpio.PWM(enA, 100)
        self.pwmB = gpio.PWM(enB, 100)
        self.pwmA.start(0)
        self.pwmB.start(0)
        pass

    def move(self, leftSpeed, rightSpeed):
        # Set speed
        self.pwmA.ChangeDutyCycle(leftSpeed)
        self.pwmB.ChangeDutyCycle(rightSpeed)
        pass

    def forward(self):
        gpio.output(in1, False)
        gpio.output(in2, True)
        gpio.output(in3, False)
        gpio.output(in4, True)
        pass

    def reverse(self):
        gpio.output(in1, True)
        gpio.output(in2, False)
        gpio.output(in3, True)
        gpio.output(in4, False)
        pass

    def gpio_stop(self):
        gpio.output(in1, False)
        gpio.output(in2, False)
        gpio.output(in3, False)
        gpio.output(in4, False)
        pass

    def cleanup(self):
        self.pwmA.stop()
        self.pwmB.stop()
        gpio.cleanup()
        exit()
        pass

    def shutdown(self):
        os.system("sudo shutdown now -h")

server = zerorpc.Server(Control())
server.bind("tcp://127.0.0.1:4242")
server.run()

