# Darius Jones
# Colin Hinton
# Kira Loomis
import os
import RPi.GPIO as gpio
import time
import serial

#  motors to  gpio
# ena = 13
# enb = 12
in1 = 17
in2 = 22
in3 = 23
in4 = 24

# setup 
gpio.setmode(gpio.BCM)
gpio.setup(in1, gpio.OUT)
gpio.setup(in2, gpio.OUT)
gpio.setup(in3, gpio.OUT)
gpio.setup(in4, gpio.OUT)
gpio.setwarnings(False)

os.system("gpio mode 23 pwm")
os.system("gpio mode 26 pwm")
os.system("gpio pwm-ms")
os.system("gpio pwmr 4000")
os.system("gpio pwmr 4095")


def forward(tf,duty1,duty2):
    command1 = "gpio pwm 23 %d" % duty1
    command2 = "gpio pwm 26 %d" % duty2

    os.system(command1)
    os.system(command2)

    gpio.output(in1, gpio.HIGH)
    gpio.output(in2, gpio.LOW)
    gpio.output(in3, gpio.HIGH)
    gpio.output(in4, gpio.LOW)
    time.sleep(tf)



def rightTurn(tf, duty):
    command1 = "gpio pwm 23 %d" % (duty)
    command2 = "gpio pwm 26 %d" % (duty)
    os.system(command1)
    os.system(command2)

    gpio.output(in1, True)
    gpio.output(in2, False)
    gpio.output(in3, False)
    gpio.output(in4, True)
    time.sleep(tf)


def get_msg():
    with serial.Serial('/dev/ttyS0', 9600) as ser:
        ser.flushInput()

        x = ser.readline().decode()
        return x


def split_directions(string_input):
    list_results = string_input.split(",")
    direction = ""
    magnitude = 0

    if len(list_results) != 2:
        # error case
        direction = "ERROR: list size = %d" % (len(list_results))
        return direction, magnitude
    else:
        direction = list_results[0]
        magnitude = list_results[1]
        return direction, magnitude


if __name__ == '__main__':

    while True:
        # print(get_msg())
        direction, magnitude = split_directions(get_msg())
        print(direction, " ", magnitude)
        if direction == "left":
            forward(1, 4000*magnitude, 4000)
        elif direction == "right":
            forward(1, 4000, magnitude*4000)
        elif direction == "straight":
            forward(1, 4000, 4000)
        else:
            rightTurn(1, 2000)
        gpio.cleanup()
