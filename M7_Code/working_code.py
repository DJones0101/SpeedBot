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
sensor.skip_frames(time = 2000)
clock = time.clock()


# assumes check has already been performed on line prior to call, to
# ensure that actually have a line => ALL ERROR HANDLING ON NOT SEEING
# LINE SHOULD BE PERFORMED PRIOR TO CALL
def get_turn_directions(line, img):
    direction_string = ""
    magnitude_string = ""

    center_x = img.width() / 2
    center_y = img.height() / 2

    horizontal_distance_from_center = 0
    vertical_slope = False

    if line.x2() - line.x1() != 0:
        slope = (line.y1() - line.y2()) / (line.x1() - line.x2())
        # y = mx + b => b = y-mx
        y_intercept = line.y1() - (slope * line.x1())
        #x = (y-b) / m
        horizontal_distance_from_center = (((img.height() / 2) - y_intercept)/ slope) - (img.width() / 2)
        # y = mx + b
        vertical_distance_from_center = ((slope * (img.width() / 2)) + y_intercept) - (img.height() / 2)
    else:
        slope = MAX_LINE_SLOPE
        vertical_slope = True
        horizontal_distance_from_center = line.x1() - (img.width() / 2)

    if vertical_slope:
        if horizontal_distance_from_center < 0:
            direction_string = "left"
        elif horizontal_distance_from_center == 0:
            direction_string = "straight"
        else:
            direction_string = "right"
    else:
        # actually a negative slope, camera inverting for some reason
        if slope > 0:
            if vertical_distance_from_center > 0:
                direction_string = "straight"
            else:
                direction_string = "left"
        # actually a positive slope
        else:
            if vertical_distance_from_center > 0:
                direction_string = "straight"
            else:
                direction_string = "right"

    if vertical_slope:
        string_magnitude = "0"
    else:
        string_magnitude = "%f" % (min(abs(slope / MAX_LINE_SLOPE), 1))

    #direction_string = "x1: %d; x2: %d, y1: %d, y2: %d" % (line.x1(), line.x2(), line.y1(), line.y2())

    return direction_string, string_magnitude
#
#def turn_instructions(horizontal_offset, line_angle_magnitude):
#   # magnitude scale: two factors:
#   #   1) slope of line (how much track is curving)
#   #       => larger factor
#   #   2) horizontal distance between line and center (how far off from line robot is)
#   #       => smaller factor
#
#   direction = "right"
#   if horizontal_offset < 0:
#       direction = "left"
#   else if horizontal_offset == 0:
#       direction = "straight"
#
#   # smaller slope => bigger turn; max slope, then == 0
#   # WANT: percentage, in range from 0 to 1
#   turn_magnitude = line_angle_magnitude
#
#
#
#

def draw_crosshair(img):
    # for i in range(10):
    x = img.width() // 2
    y = img.height() // 2
    r = (pyb.rng() % 127) + 128
    g = (pyb.rng() % 127) + 128
    b = (pyb.rng() % 127) + 128
    img.draw_cross(x, y, color = (r, g, b), size = 3, thickness = 1)


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
        offset, slope = get_turn_directions(line, img)

    #    t, r = line_to_theta_and_rho_error(line, img)
    #    new_result = (t * THETA_GAIN) + (r * RHO_GAIN)
    #    delta_result = new_result - old_result
    #    old_result = new_result

        new_time = pyb.millis()
        delta_time = new_time - old_time
        old_time = new_time

    #    p_output = new_result
    #    i_output = max(min(i_output + new_result, I_MAX), I_MIN)
    #    d_output = (delta_result * 1000) / delta_time
    #    pid_output = (P_GAIN * p_output) + (I_GAIN * i_output) + (D_GAIN * d_output)
    #
    #    output = 90 + max(min(int(pid_output), 90), -90)
    #    print_string = "Line Ok - turn %d - line t: %d, r: %d" % (output, line.theta(), line.rho())
        #print_string = "%s,%s,\n" % (offset, slope)

    else:
        print_string = "bad,bad,\r"

    print("FPS %f, %s" % (clock.fps(), print_string))

    # direction, magnitude = get_turn_directions(img, line)
    # string_directions = "%s, %s" % (direction, magnitude)
    uart.write(print_string)

