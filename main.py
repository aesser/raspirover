import time
import sys
import logging
from rrb3 import *

import board
import busio
import adafruit_bno055

def calibrate_compass(rr):
    """function to calibrate compass"""
    logging.info("calibrating compass")

    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bno055.BNO055(i2c)

    system = 0
    gyro = 0
    accel = 0
    mag = 0

    sensor.getCalibration(system, gyro, accel, mag)
    logging.debug("Sys:");
    logging.debug(system);
    logging.debug(" G:");
    logging.debug(gyro);
    logging.debug(" A:");
    logging.debug(accel);
    logging.debug(" M:");
    logging.debug(mag);

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


def main_loop():
    """The main loop controlling the robot"""
    init_wait = 1

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.info("Initialisation")
    rr = RRB3()

    calibrate_compass(rr)
    blink_lights(rr, 5)
    time.sleep(init_wait)

    logging.info("Start main loop")
    running = False
    measure_distance(rr, 1)
    measure_distance(rr, 5)
    measure_distance(rr,10)
    measure_distance(rr,20)
    while running:
        pass

if __name__ == '__main__':
    main_loop()
