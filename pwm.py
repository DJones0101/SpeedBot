
import os
import RPi.GPIO as gpio
import time


in1 = 17
in2 = 22
in3 = 23
in4 = 24

gpio.setmode(gpio.BCM)
gpio.setup(in1, gpio.OUT)
gpio.setup(in2, gpio.OUT)
gpio.setup(in3, gpio.OUT)
gpio.setup(in4, gpio.OUT)
gpio.setwarnings(False)

os.system("gpio mode 23 pwm")
os.system("gpio mode 26 pwm")
os.system("gpio pwm-ms")
os.system("gpio pwmr 100")
os.system("gpio pwmc 82") #82


try:
	count = 0
	while True:
		command1 = "gpio pwm 23 %d" % count
		command2 = "gpio pwm 26 %d" % count
		os.system(command1)
		os.system(command2)
		time.sleep(.01)
		count += 1
		print("duty : %d" %count)
		#count += .1
		#if count == 2: break

except KeyboardInterrupt:
	gpio.cleanup()