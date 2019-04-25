
# Darius Jones
# Colin Hinton
# Kira Loomis


import RPi.GPIO as gpio
import time 
import SpeedBot.m7 as m7


#  motors to  gpio
ena = (5,6)
enb = (13,19)
in1 = 17
in2 = 22
in3 = 23
in4 = 24 

# encoders to gpio
right = 16
left =  20

# setup 
gpio.setmode(gpio.BCM)
gpio.setup(right,gpio.IN,pull_up_down=gpio.PUD_UP)
gpio.setup(left,gpio.IN,pull_up_down=gpio.PUD_UP)
gpio.setup(ena[0],gpio.OUT)
gpio.setup(ena[1],gpio.OUT)
gpio.setup(enb[0],gpio.OUT)
gpio.setup(enb[1],gpio.OUT)
gpio.setup(in1,gpio.OUT)
gpio.setup(in2,gpio.OUT)
gpio.setup(in3,gpio.OUT)
gpio.setup(in4,gpio.OUT)
gpio.output(ena[0],True)
gpio.output(ena[1],True)
gpio.output(enb[0],True)
gpio.output(enb[1],True)
gpio.setwarnings(False)

leftEncoder = gpio.input(left)
rightEncoder = gpio.input(right)


def forward(tf):

	gpio.output(in1,True)
	gpio.output(in2,False)
	gpio.output(in3,True)
	gpio.output(in4,False)
	time.sleep(tf)
	

def backward(tf):
	gpio.output(in1,False)
	gpio.output(in2,True)
	gpio.output(in3,False)
	gpio.output(in4,True)
	time.sleep(tf)
	
def rightTurn(tf):
	gpio.output(in1,True)
	gpio.output(in2,False)
	gpio.output(in3,False)
	gpio.output(in4,True)
	time.sleep(tf)

def leftTurn(tf):
	gpio.output(in1,False)
	gpio.output(in2,True)
	gpio.output(in3,True)
	gpio.output(in4,False)
	time.sleep(tf)

def PWM_briefTest(tf):
	# Tested version:
	p = gpio.PWM(in1, 31250)
	q = gpio.PWM(in3, 31250)
	p.start(.75)
	q.start(.75)

	time.sleep(tf)

	p.stop()
	q.stop()

	# # If have issues w/ continual stops, this was suggested:
	# # p.ChangeDutyCycle(0)
	# # q.ChangeDutyCycle(0)	

def PWM_robustTest(tf):

	leftForward = gpio.PWM(in1, 31250)
	leftBackward = gpio.PWM(in2, 31250)
	rightForward = gpio.PWM(in3, 31250)
	rightBackward = gpio.PWM(in4, 31250)

	# Forward:
	leftForward.start(.75)
	rightForward.start(.75)

	time.sleep(tf)

	leftForward.stop()
	rightForward.stop()

	# Backward:
	leftBackward.start(.75)
	rightBackward.start(.75)

	time.sleep(tf)

	leftBackward.stop()
	rightBackward.stop()

	# Right Turn
	leftForward.start(.75)
	rightBackward.start(.75)

	time.sleep(tf)

	leftForward.stop()
	rightBackward.stop()

	# Left Turn
	leftBackward.start(.75)
	rightForward.start(.75)

	time.sleep(tf)

	leftBackward.stop()
	rightForward.stop()

	# Arcs
	# # Right Arc
	rightForward.start(.60)
	leftForward.start(.75)

	time.sleep(tf)

	# # Left Arc
	rightForward.ChangeDutyCycle(.75)
	leftForward.ChangeDutyCycle(.60)

	time.sleep(tf)

	rightForward.stop()
	leftForward.stop()



if __name__ == '__main__':

	PWM_briefTest(10)
	#count = 0
	#while True:
	#	
	#	print("%d  %s"  %(count,  m7.get_msg()))
	#	count += 1
	gpio.cleanup()
