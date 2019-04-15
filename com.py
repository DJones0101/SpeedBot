import serial

with serial.Serial('/dev/ttyS0', 9600, timeout=1) as ser:
	while True:
		x = ser.readline()
		print(x)
