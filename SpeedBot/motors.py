import RPi.GPIO as gpio
import time 
import math

# vr = (2V + WL)/2R
# vl = (2V - WL)/2R

# V= speed , W= angular velocity

ena = (5)
enb = (13)
in1 = 17
in2 = 22
in3 = 23
in4 = 24 
right = 16
left =  20
gpio.setmode(gpio.BCM)
gpio.setup(right,gpio.IN,pull_up_down=gpio.PUD_UP)
gpio.setup(left,gpio.IN,pull_up_down=gpio.PUD_UP)
gpio.setup(ena,gpio.OUT)
gpio.setup(enb,gpio.OUT)

gpio.setup(in1,gpio.OUT)
gpio.setup(in2,gpio.OUT)
gpio.setup(in3,gpio.OUT)
gpio.setup(in4,gpio.OUT)
gpio.output(ena,True)
gpio.output(enb,True)


leftEncoderLast = gpio.input(left)
rightEncoderLast = gpio.input(right)


R = 6.2
L = 15.5
leftForward = gpio.PWM(in1, 31250)
leftBackward = gpio.PWM(in2, 31250)
rightForward = gpio.PWM(in3, 31250)
rightBackward = gpio.PWM(in4, 31250)

tR = gpio.PWM(ena, 31250) 
tL = gpio.PWM(enb, 31250)
tR.start(0)
tL.start(0)

leftForward.start(0)
leftBackward.start(0)
rightBackward.start(0)
rightForward.start(0)
gpio.setwarnings(False)



def move(v, w, tf):
	
	gpio.setwarnings(False)
	vr = ((2 * v) + (w * L))/(2 * R)
	vl = ((2 * v) - (w * L))/(2 * R)

	# tR.ChangeDutyCycle(100)
	# tL.ChangeDutyCycle(100)
	# rightForward.ChangeDutyCycle(100)
	# leftForward.ChangeDutyCycle(100)

	time.sleep(tf)
	leftForward.stop()
	rightForward.stop()

	print("vr :%d, vl :%d " %(vr, vl))
	gpio.cleanup()


