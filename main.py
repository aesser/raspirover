import time
from rrb3 import *

rr = RRB3()

led1 = 0
led2 = 1

while True:
    rr.set_led1(led1)
    rr.set_led2(1)

    led_tmp = led2
    led2 = led1
    led1 = led_tmp

    time.sleep(0.02)
