import time
import logging
from rrb3 import *


def calibrate_compass(rr):
    """function to calibrate compass"""
    pass


def blink_lights(rr, n_blinks, sleep_time=0.5):
    """show blinking lights"""
    led1 = 0
    led2 = 1
    for i in range(n_blinks):
        rr.set_led1(led1)
        rr.set_led2(led2)

        tmp = led2
        led2 = led1
        led1 = tmp

        time.sleep(sleep_time)


def measure_distance():
    """measure distance and average"""
    pass


def go_direction():
    """functioni to run the robot a ceratin direction"""
    pass


def turn():
    """functio to turn the robot"""
    pass


def main_loop():
    """The main loop controlling the robot"""
    rr = RRB3()

    calibrate_compass(rr)
    blink_lights(rr, 20)
    time.sleep(20)

    running = False
    while running:
        pass

if __name__ == '__main__':
    main_loop()