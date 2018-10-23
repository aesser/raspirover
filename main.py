import time
import sys
import enum
import logging
from rrb3 import *

from Adafruit_BNO055 import BNO055

def signum(x):
    return (x > 0) - (x < 0)

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


def measure_distance(rr, n_distance, sleep_time=0.0001):
    """measure distance and average"""
    sum_distance = 0 
    for i in range(n_distance):
        sum_distance += rr.get_distance()
        time.sleep(sleep_time)
    distance = sum_distance/n_distance
    logging.info("Measured distance is {} (average of N{})".format(distance, n_distance))
    return distance



def turn(rr, bno, target_heading, tol=0.5):
    """functio to turn the robot"""
    max_speed = 0.6
    min_speed = 0.3
    current_heading = get_heading(bno)

    
    while abs(target_heading-current_heading) > tol:

        current_heading = get_heading(bno)
	degree_direction = target_heading-current_heading
        if abs(degree_direction) > 180:
	    if degree_direction > 180:
	    	degree_direction -= 360
	    else:
	        degree_direction += 360
	turning_speed = max(max_speed*abs(degree_direction)/180., min_speed)
	positiv_rot = signum(degree_direction) > 0
	logging.info("target_heading {}, current_heading {}, degree_direction {}, turning speed {}, rot {}".format(target_heading, current_heading, degree_direction, turning_speed, positiv_rot))
        rr.set_motors(abs(turning_speed), int(positiv_rot),
		      abs(turning_speed), int(not positiv_rot))

		
	
    rr.set_motors(0, 0, 0, 0)
	

def get_heading(bno, tol=1.e-1):
    """function to return heading of robot"""
    prev_heading, heading = bno.read_euler()[0], bno.read_euler()[0]
    while abs(heading - prev_heading) > tol:
	prev_heading, heading = heading, bno.read_euler()[0]
    logging.debug("Measured heading is {}".format(heading))
    return heading

def correct_heading(target):
    if target < 0:
	return target+360
    if target > 360:
	return target - 360
    return target


def main_loop():
    """The main loop controlling the robot"""
    init_wait = 5
    max_speed = 0.8
    min_distance = 10
    traveltime = 0.10
    backtime = 0.25

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.info("Initialisation")
    rr = RRB3()

    bno = BNO055.BNO055(serial_port='/dev/ttyUSB0', rst=18)
    if not bno.begin():
    	raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

    calibrate_compass(bno)
    blink_lights(rr, 5)
    time.sleep(init_wait)

    logging.info("Start main loop")
    running = True

    
    start_heading = get_heading(bno)
    target_heading=start_heading
    turn(rr, bno, target_heading)	
    while running:
        
	rr.set_motors(max_speed, 0, max_speed, 0)
	time.sleep(traveltime)
	turn(rr, bno, target_heading)	
	
	distance = measure_distance(rr, 20)
	logging.info(distance)
	if distance < min_distance:

            rr.set_motors(max_speed, 1, max_speed, 1)
	    time.sleep(backtime)  
            turn(rr, bno, target_heading)
            distance = measure_distance(rr, 20)
	    if distance < min_distance*2:
		    
                    t_b = correct_heading(get_heading(bno)-180)
		    turn(rr, bno, t_b)
                    rr.set_motors(max_speed, 1, max_speed, 1)
                    time.sleep(backtime*5) 
	            rr.set_motors(max_speed, 1, 0, 1)
	            time.sleep(backtime) 
		    rr.set_motors(0, 1, max_speed, 1)
                    time.sleep(backtime)
                    rr.set_motors(0, 0, 0, 0) 
                    time.sleep(0.001)
		    target_heading = get_heading(bno)
                    rr.set_motors(0.3, 0, 0.3, 0)
                    time.sleep(backtime) 
                    rr.set_motors(0, 0, 0, 0)

		    t_l = correct_heading(target_heading-90)
		    turn(rr, bno, t_l)
		    d_l = measure_distance(rr, 20)
	            t_r = correct_heading(target_heading+90)
		    turn(rr, bno, t_r)
		    d_r = measure_distance(rr, 20)
		    if d_l > d_r:
			target_heading = t_l
		    else:
			target_heading = t_r

		    t_b = correct_heading(target_heading)
		    turn(rr, bno, t_b)
                    rr.set_motors(max_speed, 1, max_speed, 1)
                    time.sleep(backtime*5) 
	            rr.set_motors(max_speed, 1, 0, 1)
	            time.sleep(backtime) 
		    rr.set_motors(0, 1, max_speed, 1)
                    time.sleep(backtime)
                    rr.set_motors(0, 0, 0, 0) 
			
                    rr.set_motors(0.3, 0, 0.3, 0)
                    time.sleep(backtime) 
                    rr.set_motors(0, 0, 0, 0)
            
        

if __name__ == '__main__':
    main_loop()
