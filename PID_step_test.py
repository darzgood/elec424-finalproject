### Pid Step Test ###
# Darrell Good
# Rice University
# 11-21-2023
# Uses Motors2.py file with methods
import time
from datetime import datetime
import bno055_read
import Motors2

PWM_FREQ = 50
NEG_DUTY = 5
POS_DUTY = 10
ZERO_DUTY = 7.5

CHANNEL0 = 0
CHANNEL1 = 1

m1 = Motors2.Motor()  # Input arguments, changed so there are none
m1.pwm_init(PWM_FREQ, PWM_FREQ)

m1.pwm_output(ZERO_DUTY, chan=CHANNEL0)
m1.pwm_output(ZERO_DUTY, chan=CHANNEL1)

if __name__ == "__main__":
    for i in range(10):
        print("{0} \t {1} \t {2}".format(datetime.now(), 0, bno055_read.read()))
        time.sleep(1)

m1.pwm_output(POS_DUTY, chan=CHANNEL0)
m1.pwm_output(NEG_DUTY, chan=CHANNEL1)

for i in range(10):
    print("{0} \t {1} \t {2}".format(datetime.now(), 1, bno055_read.read()))
    time.sleep(1)

m1.pwm_output(POS_DUTY, chan=CHANNEL0)
m1.pwm_output(NEG_DUTY, chan=CHANNEL1)

for i in range(10):
    print("{0} \t {1} \t {2}".format(datetime.now(), 1, bno055_read.read()))
    time.sleep(1)




