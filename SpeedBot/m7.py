#!/usr/bin/env python

__author__ = "Darius Jones"
__credits__ = ["Kira Loomis", "Colin Hinton"]

"""
OpenMV M7 camera is connected to the RPI's UART pins at GPIO 14 and 15. 
RPi will receive instructions from the M7 for motor controll. 

"""

import serial
import time


def get_msg():

	serial.Serial.open()
	with serial.Serial('/dev/ttyS0', 9600, timeout=1) as ser:
			ser.flushInput()
			time.sleep(1)
			x = ser.readline()
			#print(x)
			ser.Serial.close()
			return x


def print_test():
	x = "Hello World!"
	print(x)
