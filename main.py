import time
import logging
from rrb3 import *

rr = RRB3()

led1 = 0
led2 = 1

canRun = True


logger = logging.getLogger()
counter = 0
while canRun:
    try:

        rr.set_led1(led1)
        rr.set_led2(led2)

        tmp = led2
        led2 = led1
        led1 = tmp

        time.sleep(0.5)

        counter += 1
        if counter > 20:
            break

        logger.info("switch")
    except RuntimeError:
        logger.error("Runtime Error")

logger.info("Bye")

