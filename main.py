from simple_pid import PID
import bno055_read
import sys

desired_angle = (int(sys.argv[1]) + bno055_read.euler()[0]) % 360

pid = PID(1, 0.1, 0.05, setpoint=desired_angle)

select = 2

if bno055_read.euler()[select] - desired_angle > 180:
    offset = +180
elif bno055_read.euler()[select] - desired_angle < -180:
    offset = -180
else:
    offset = 0

from rpi_hardware_pwm import HardwarePWM


# Duty cycle values
# PWM pins for default Device Tree Overlay is channel0 -> Pin 18
# channel1 -> Pin 13

# Constants
BACK_PWM = 5
STOP_PWM = 7.5
FORWARD_PWM = 10
OFF_PWM = 0

def pwm_init(frequency1, frequency2):
    pwm0 = HardwarePWM(pwm_channel=0, hz=frequency1)
    pwm1 = HardwarePWM(pwm_channel=1, hz=frequency2)
    pwm = (pwm0, pwm1)
    pwm[0].start(OFF_PWM)
    pwm[1].start(OFF_PWM)
    return pwm

def pwm_output(pwm_channels, duty_cycle, channel):
    # Note that pwm input is a tupe with each pwm channel
    pwm_channels[channel].stop()
    pwm_channels[channel].start(duty_cycle)
    return 0

pwm = pwm_init(20, 1)
#pwm_output(pwm, STOP_PWM, 1)
#pwm_output(pwm, BACK_PWM, 0)

# Assume we have a system we want to control in controlled_system
#v = controlled_system.update(0)
pwm_output(pwm, STOP_PWM, 0)


while True:
    # Compute new output from the PID according to the systems current value
    angle = bno055_read.euler()[select]

    if abs(angle - desired_angle) > 180:
        angle += offset

    control = pid(angle)
    print(control)

    # Feed the PID output to the system and get its current value
    #    v = controlled_system.update(control)
    pwm_output(pwm, control, 0)
