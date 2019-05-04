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
# gpio.output(ena,gpio.HIGH)
# gpio.output(enb,gpio.HIGH)
gpio.setwarnings(False)

os.system("gpio mode 23 pwm")
os.system("gpio mode 26 pwm")
os.system("gpio pwm-ms")
os.system("gpio pwmr 4000")
os.system("gpio pwmr 4095")


def forward(tf):
    command1 = "gpio pwm 23 %d" % (4000)
    command2 = "gpio pwm 26 %d" % (3000)

    os.system(command1)
    os.system(command2)

    gpio.output(in1, gpio.HIGH)
    gpio.output(in2, gpio.LOW)
    gpio.output(in3, gpio.HIGH)
    gpio.output(in4, gpio.LOW)
    time.sleep(tf)


def backward(tf):
    command1 = "gpio pwm 23 %d" % (duty)
    command2 = "gpio pwm 26 %d" % (duty)
    os.system(command1)
    os.system(command2)

    gpio.output(in1, False)
    gpio.output(in2, True)
    gpio.output(in3, False)
    gpio.output(in4, True)
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


def leftTurn(tf, duty):
    command1 = "gpio pwm 23 %d" % (duty)
    command2 = "gpio pwm 26 %d" % (duty)
    os.system(command1)
    os.system(command2)

    gpio.output(in1, False)
    gpio.output(in2, True)
    gpio.output(in3, True)
    gpio.output(in4, False)
    time.sleep(tf)


def arcLeft(tf):
    command1 = "gpio pwm 23 %d" % (4000)
    command2 = "gpio pwm 26 %d" % (2000)
    os.system(command1)
    os.system(command2)

    gpio.output(in1, False)
    gpio.output(in2, True)
    gpio.output(in3, True)
    gpio.output(in4, False)
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

    else:
        direction = list_results[0]
        magnitude = list_results[1]
        return direction, magnitude


if __name__ == '__main__':

    while True:
        # print(get_msg())
        direction, magnitude = split_directions(get_msg())
        print(direction, " ", magnitude)
        gpio.cleanup()
