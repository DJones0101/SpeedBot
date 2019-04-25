#!/usr/bin/env python

__author__ = "Darius Jones"
__credits__ = ["Kira Loomis", "Colin Hinton"]

"""
OpenMV M7 camera is connected to the RPI's UART pins at GPIO 14 and 15. 
RPi will receive instructions from the M7 for motor control. 

"""

import serial
import time

class M7:
	def __init__():
		self.connection = '/dev/ttyS0'



	def get_msg(baudRate):

		#serial.Serial.open()
		with serial.Serial(self.connection, baudRate) as ser:
				while ser.in_waiting:
					time.sleep(.1)
					ser.flushInput()
					time.sleep(.1)
					x = ser.readline().decode()
			return x

	def send_msg(baudRate, msg):
		
		with serial.Serial(self.connection, baudRate) as ser:
			ser.flushInput()
			ser.flushOutput()
			ser.write(msg)

