# Robust Linear Regression Example
#
# This example shows off how to use the get_regression() method on your OpenMV Cam
# to get the linear regression of a ROI. Using this method you can easily build
# a robot which can track lines which all point in the same general direction
# but are not actually connected. Use find_blobs() on lines that are nicely
# connected for better filtering options and control.
#
# We're using the robust=True argument for get_regression() in this script which
# computes the linear regression using a much more robust algorithm... but potentially
# much slower. The robust algorithm runs in O(N^2) time on the image. So, YOU NEED
# TO LIMIT THE NUMBER OF PIXELS the robust algorithm works on or it can actually
# take seconds for the algorithm to give you a result... THRESHOLD VERY CAREFULLY!

THRESHOLD = (0, 100) # Grayscale threshold for dark things...
BINARY_VISIBLE = True # Does binary first so you can see what the linear regression
                      # is being run on... might lower FPS though.

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA) # 80x60 (4,800 pixels) - O(N^2) max = 2,3040,000.
sensor.skip_frames(time = 2000)     # WARNING: If you use QQVGA it may take seconds
clock = time.clock()                # to process a frame sometimes.

while(True):
    clock.tick()
    img = sensor.snapshot().binary([THRESHOLD]) if BINARY_VISIBLE else sensor.snapshot()

    for i in range(10):
        x = (img.width()//2)
        y = (img.height()//2)
        r = (pyb.rng() % 127) + 128
        g = (pyb.rng() % 127) + 128
        b = (pyb.rng() % 127) + 128

    # If the first argument is a scaler then this method expects
    # to see x and y. Otherwise, it expects a (x,y) tuple.
    img.draw_cross(x, y, color = (r, g, b), size = 10, thickness = 2)

    # Returns a line object similar to line objects returned by find_lines() and
    # find_line_segments(). You have x1(), y1(), x2(), y2(), length(),
    # theta() (rotation in degrees), rho(), and magnitude().
    #
    # magnitude() represents how well the linear regression worked. It means something
    # different for the robust linear regression. In general, the larger the value the
    # better...
    line = img.get_regression([(255,255) if BINARY_VISIBLE else THRESHOLD], robust = True)

    if (line): img.draw_line(line.line(), color = 127)
    #print("FPS %f, mag = %s" % (clock.fps(), str(line.magnitude()) if (line) else "N/A"))

    widthValue = ((img.height()//2)/((line.y2()-line.y1())/line.x2()-line.x1())) - img.width(//2)
    print("Distance from center %f" % (widthValue))

# About negative rho values:
#
# A [theta+0:-rho] tuple is the same as [theta+180:+rho].
