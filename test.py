
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





if __name__ == '__main__':


	forward(5)
	backward(5)
	
   
    print("Writing to display")
    display.lcd_display_string("       SpeedBot!", 1) # Write line of text to first line of display
    display.lcd_display_string('Comp 470', 2) # Write line of text to second line of display
    time.sleep(10)                                     # Give time for the message to be read
    display.lcd_display_string("Stuff", 3)  # Refresh the first line of display with a different message
    display.lcd_display_string("bye!!!", 4) 
    time.sleep(10)                                     # Give time for the message to be read
    display.lcd_clear()                               # Clear the display of any data
    time.sleep(2)                                     # Give time for the message to be read
    print("Cleaning up!")
    display.lcd_clear()
    gpio.cleanup()