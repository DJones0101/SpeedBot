# SpeedBot
---

## L298N to RPi
---
The L298N's ena and enb pins enable voltage to be supplied to the connected motors. Pins in1 - in4 are used
to control the motors. L298N's pins are wired to the RPi as follows:


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
 
 RPi's pinout for futher refernce.

![alt text][rpi]

[rpi]: https://github.com/DJones0101/SpeedBot/blob/master/img/pi_pinout.png

---
## M7 to RPi 