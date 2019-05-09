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


error_count = 0


def forward(tf, duty1, duty2):

    
    command1 = "gpio pwm 23 %d" % duty1
    command2 = "gpio pwm 26 %d" % duty2

    os.system(command1)
    os.system(command2)

    gpio.output(in1, gpio.HIGH)
    gpio.output(in2, gpio.LOW)
    gpio.output(in3, gpio.HIGH)
    gpio.output(in4, gpio.LOW)
    time.sleep(1)


    

def stop(tf):
    command1 = "gpio pwm 23 %d" % 0
    command2 = "gpio pwm 26 %d" % 0

    os.system(command1)
    os.system(command2)

    gpio.output(in1, gpio.LOW)
    gpio.output(in2, gpio.LOW)
    gpio.output(in3, gpio.LOW)
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
    with serial.Serial('/dev/ttyS0', 9600,timeout=2.0) as ser:
        msg = []
        count = 0 
        ser.flushInput()
        while True:
            msg.append(ser.read(1).decode())
            time.sleep(0.01)
            if msg[count] == '\n':
                #print(msg)
                break
            count += 1            
        
        return "".join(msg)



def split_directions(string_input):
    list_results = string_input.split(",")
    direction = ""
    magnitude = 0
    # print(string_input)
    #print(list_results)
    # print(type(list_results[0]))
    # print(type(list_results[1]))
    # do we need dummy variable for /n or /r
    # should it be != 4 
    if len(list_results) != 3:
        # error case
        #direction = "ERROR: list size = %d" % (len(list_results))
        
        return direction, magnitude
    else:
        direction = list_results[0]
        magnitude = list_results[1]
        # print(direction)
        # print(magnitude)
        return direction, magnitude


if __name__ == '__main__':
    try:
        while True:
            commands = get_msg()

            #print(commands)
            # direction, magnitude = split_directions(commands)
            # print(direction, " ", magnitude)
            # time.sleep(.1)

            length = len(commands)
            string_index = length - 12

            if string_index >= 0:
                commands = commands[string_index:]
                magnitude = int(commands[4:len(commands)-2])
                magnitude = magnitude / (10 ** 6)
                print(commands[0])
                print(magnitude)

            if commands[0] == "s":
                forward(1, 4000, 4000)
            elif commands[0] == "r":
                forward(1, 4000, magnitude * 4000)
            elif commands[0] == "l":
                forward(1, 4000*magnitude, 4000)
            else:
                if error_count >= 3:
                    rightTurn(1, 2000)
                    stop(1)
                    error_count = 0
                else:
                    error_count += 1
    except KeyboardInterrupt:
        gpio.cleanup()