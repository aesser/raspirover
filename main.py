import time
import sys
import logging
from rrb3 import *

from Adafruit_BNO055 import BNO055

def calibrate_compass(bno):
    """function to calibrate compass"""
    logging.info("calibrating compass")
    calib_status = 0
    while calib_status != 3:
    	# Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    	calib_status = bno.get_calibration_status()[0]
    logging.info("calibrating compass .. done")

system = gyro = accel = mag = 0;
def blink_lights(rr, n_blinks, sleep_time=0.5):
    """show blinking lights"""
    logging.info("blinking lights")
    led1 = 0
    led2 = 1
    for i in range(n_blinks):
        rr.set_led1(led1)
        rr.set_led2(led2)

        tmp = led2
        led2 = led1
        led1 = tmp

        time.sleep(sleep_time)


def measure_distance(rr, n_distance, sleep_time=0.001):
    """measure distance and average"""
    sum_distance = 0 
    for i in range(n_distance):
        sum_distance += rr.get_distance()
        time.sleep(sleep_time)
    distance = sum_distance/n_distance
    logging.debug("Measured distance is {} (average of N{})".format(distance, n_distance))
    return distance

def go_direction():
    """functioni to run the robot a ceratin direction"""
    pass


def turn():
    """functio to turn the robot"""
    pass

def get_heading(bno, tol=1.e-1):
    """function to return heading of robot"""
    prev_heading, heading = bno.read_euler()[0], bno.read_euler()[0]
    while abs(heading - prev_heading) > tol:
	prev_heading, heading = heading, bno.read_euler()[0]
    logging.debug("Measured heading is {}".format(heading))
    return heading

def main_loop():
    """The main loop controlling the robot"""
    init_wait = 1

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.info("Initialisation")
    rr = RRB3()

    bno = BNO055.BNO055(serial_port='/dev/ttyUSB0', rst=18)
    if not bno.begin():
    	raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

    calibrate_compass(bno)
    blink_lights(rr, 5)
    time.sleep(init_wait)

    logging.info("Start main loop")
    running = False
    measure_distance(rr, 1)
    measure_distance(rr, 5)
    measure_distance(rr,10)
    measure_distance(rr,20)

    get_heading(bno)

    while running:
        pass

if __name__ == '__main__':
    main_loop()
