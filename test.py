
# Darius Jones
# Colin Hinton
# Kira Loomis

import lcddriver 
import RPi.GPIO as gpio
import time 

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

lefEncoder = gpio.input(left)
rightEncoder = gpio.input(right)

display = lcddriver.lcd()


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

def gradualLeftArc(tf):
	counter = 0

	gpio.output(in2,False)
	gpio.output(in3,True)
	gpio.output(in4,False)


	timeRemaining = tf
	timeSegment = .02

	while timeRemaining > 0:
		if (counter % 2) == 0:
			gpio.output(in1,False)
		else:
			gpio.output(in1, True)

		time.sleep(timeSegment)

		timeRemaining -= timeSegment
		counter += 1


def gradualRightArc(tf):
	counter = 0

	gpio.output(in1,True)
	gpio.output(in2,False)
	gpio.output(in4,False)


	timeRemaining = tf
	timeSegment = .02

	while timeRemaining > 0:
		if (counter % 2) == 0:
			gpio.output(in3,False)
		else:
			gpio.output(in3, True)

		time.sleep(timeSegment)

		timeRemaining -= timeSegment
		counter += 1	



if __name__ == '__main__':



	#display.lcd_display_string("SpeedBot", 1)
	#time.sleep(5)
	#display.lcd_display_string("Moving forward for 5 senconds", 2)
	#time.sleep(10)
	gradualRightArc(5)
	#display.lcd_display_string("Moving backward for 5 senconds", 1)
	#time.sleep(10)
	#rightTurn(5)
	#time.sleep(10)
	#display.lcd_clear()
	gpio.cleanup()
	
