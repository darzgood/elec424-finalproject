# Current PID step test uses Motors2.py file which may be redundant with the PWM functions
# In pwm_test. This code doesn't make use of the class and can be used for a simple PWM output
# Changes were added to the motors class if the other PID_step_test file wants to be used

from pwm_test import pwm_init, pwm_output
import bno055_read
import time
from datetime import datetime
PWM_FREQ = 50
NEG_DUTY = 5
POS_DUTY = 10
ZERO_DUTY = 7.5

CHANNEL0 = 0
CHANNEL1 = 1

motor_pwm = pwm_init(PWM_FREQ, PWM_FREQ)  # Sets PWM frequency to 50 Hz for each channel
pwm_output(motor_pwm, ZERO_DUTY, CHANNEL0)  # Also note that the initialization starts at zero duty cycle
pwm_output(motor_pwm, ZERO_DUTY, CHANNEL1)

# For both of these, bno055_read.read() is undefined, replace with appropriate code
for i in range(10):
    print("{0} \t {1} \t {2}".format(datetime.now(), 0, bno055_read.read()))
    time.sleep(1)

pwm_output(motor_pwm, POS_DUTY, channel=0)
pwm_output(motor_pwm, NEG_DUTY, channel=1)

for i in range(10):
    print("{0} \t {1} \t {2}".format(datetime.now(), 1, bno055_read.read()))  # Read is not a function, need to change
    time.sleep(1)

pwm_output(motor_pwm, POS_DUTY, channel=0)
pwm_output(motor_pwm, NEG_DUTY, channel=1)

for i in range(10):
    print("{0} \t {1} \t {2}".format(datetime.now(), 1, bno055_read.read()))
    time.sleep(1)