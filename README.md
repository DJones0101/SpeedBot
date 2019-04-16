# SpeedBot


 RPi's pinout for reference.

![alt text][rpi]

[rpi]: https://github.com/DJones0101/SpeedBot/blob/master/img/pi_pinout.png

## L298N to RPi
---
The L298N's ena and enb pins enable voltage to be supplied to the connected motors. GPIO pins in1 - in4 are used to control the motors. L298N's pins are wired to the RPi as follows:


```python
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
```
 


---
## M7 to RPi 

The M7 is physically connected to The RPi at GPIO pins 14 and 15 (UART), since these are (UART) aka serial we have to communicate with the M7 by using the code below. 

Note: use sudo raspi-config to enable serial and disable login with serial.

(time.sleep(.1) may not be needed,  need to do more testing)

```python

with serial.Serial('/dev/ttyS0', 9600) as ser:
			while ser.in_waiting:
				time.sleep(.1)
			ser.flushInput()
			time.sleep(.1)
			x = ser.readline().decode()
			return x

```


