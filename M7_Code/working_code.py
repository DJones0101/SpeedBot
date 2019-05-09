BINARY_VIEW = True
GRAYSCALE_THRESHOLD = (240, 255)
MAG_THRESHOLD = 4
THETA_GAIN = 40.0
RHO_GAIN = -1.0
P_GAIN = 0.7
I_GAIN = 0.0
I_MIN = -0.0
I_MAX = 0.0
D_GAIN = 0.1
STEERING_SERVO_INDEX = 0
MAX_LINE_SLOPE = 12

import sensor, image, time, math, pyb, lcd
from machine import I2C, Pin
from pyb import UART

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.skip_frames(time=2000)
clock = time.clock()


# assumes check has already been performed on line prior to call, to
# ensure that actually have a line => ALL ERROR HANDLING ON NOT SEEING
# LINE SHOULD BE PERFORMED PRIOR TO CALL

def find_error_distance(line, img):
    direction_string = ""
    magnitude_string = ""

    if line.x2() - line.x1() != 0:
        slope = (line.y1() - line.y2()) / (line.x1() - line.x2())
        # y = mx + b => b = y-mx
        y_intercept = line.y1() - (slope * line.x1())
        # x = (y-b) / m
        error_position = ((img.height() - y_intercept) / slope)
        if error_position == 0:
            direction_string = "s"
            magnitude_string = 0
        elif error_position > (img.width() / 2):
            direction_string = "r"
            error_position = error_position - img.width() / 2
            magnitude_string = error_position
        else:
            direction_string = "l"
            error_position = img.width() / 2 - error_position
            magnitude_string = error_position
    else:
        if line.x1() > (img.width() / 2):
            direction_string = "r"
            error_position = line.x1() - img.width() / 2
            magnitude_string = error_position
        elif line.x1() < (img.width() / 2):
            direction_string = "l"
            error_position = img.width() / 2 - line.x1()
            magnitude_string = error_position
        else:
            direction_string = "s"
            magnitude_string = 0

    return direction_string, magnitude_string


def draw_crosshair(img):
    # for i in range(10):
    x = img.width() // 2
    y = img.height() # crosshair may break
    r = (pyb.rng() % 127) + 128
    g = (pyb.rng() % 127) + 128
    b = (pyb.rng() % 127) + 128
    img.draw_cross(x, y, color=(r, g, b), size=3, thickness=1)


old_result = 0
old_time = pyb.millis()
i_output = 0
output = 90

uart = UART(3, 9600)

while True:
    clock.tick()
    img = sensor.snapshot().histeq()
    if BINARY_VIEW:
        img.binary([GRAYSCALE_THRESHOLD])
        img.erode(1)

    line = img.get_regression([(255, 255)], robust=True)
    print_string = ""

    draw_crosshair(img)

    if line and (line.magnitude() >= MAG_THRESHOLD):
        img.draw_line(line.line(), color=127)

        # for testing purposes, to be ultimately replaced w/turn direction call
        direction, error_model = find_error_distance(line, img)
        magnitude = "%.6f" % (error_model / (10 ** 6))

        new_time = pyb.millis()
        delta_time = new_time - old_time
        old_time = new_time

        print_string = "%s,%s,\n" % (direction, magnitude)

    else:
        print_string = "bad,bad,\r"

    print("FPS %f, %s" % (clock.fps(), print_string))

    # direction, magnitude = get_turn_directions(img, line)
    # string_directions = "%s, %s" % (direction, magnitude)
    uart.write(print_string)
