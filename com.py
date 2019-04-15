import serial
import time


with serial.Serial('/dev/ttyS0', 9600, timeout=1) as ser:
		ser.flushInput()
		time.sleep(1)
		x = ser.readline()
		print(x)
