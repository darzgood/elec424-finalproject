from simple_pid import PID
import bno055_read
import sys
import time
import atexit



select = 0

desired_angle = (int(sys.argv[1]) + bno055_read.euler()[select]) % 360

#pid = PID(.1, 0.01, 0.005, setpoint=desired_angle)
pid = PID(.1, 0, 0, setpoint=desired_angle)


pid.output_limits = (-1.5, 1.5)



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

def pwm_drive(pwm_channels, duty_cycle, channel):
    pwm_channels[channel].change_duty_cycle(duty_cycle)
    return 0

def arm_motors(pwm):
    pwm_output(pwm, OFF_PWM, 1)
    pwm_output(pwm, OFF_PWM, 0)
    time.sleep(1)
    pwm_output(pwm, FORWARD_PWM, 1)
    pwm_output(pwm, FORWARD_PWM, 0)
    time.sleep(1)
    pwm_output(pwm, STOP_PWM, 1)
    pwm_output(pwm, STOP_PWM, 0)
    time.sleep(1)

def wrap_angle(angle, desired):
    if angle - desired > 180:
        offset = -360
    elif angle - desired < -180:
        offset = +360
    else:
        offset = 0
    return offset



pwm = pwm_init(46.7, 46.7)
arm_motors(pwm)

def exit_handler():
    pwm[0].stop()
    pwm[1].stop()

atexit.register(exit_handler)

#pwm_output(pwm, STOP_PWM, 1)
#pwm_output(pwm, BACK_PWM, 0)

# Assume we have a system we want to control in controlled_system
#v = controlled_system.update(0)

time.sleep(2)
vals = []
while True:
    # Compute new output from the PID according to the systems current value
    angle = bno055_read.euler()[select]
    heading = bno055_read.mag()

    if angle is None:
        continue
    if not (0 <= angle <= 360):
        continue
    angle += wrap_angle(angle, desired_angle)

    vals.append(angle)
    if len(vals) < 10:
        continue
    else:
        angle = sum(vals)/len(vals)
        vals = []

    control = pid(angle)
    print("Target: {}, \t Current: {}, \t PID: {}, \t Compass Heading: {}".format(round(desired_angle,2), round(angle,2), round(control,2), heading))

#    if (control > FORWARD_PWM - STOP_PWM):
#	control = FORWARD_PWM - STOP_PWM
#    else if (control < -2.5):
#	control = -2.5


    # Feed the PID output to the system and get its current value
    #    v = controlled_system.update(control)
    pwm_drive(pwm, STOP_PWM - control, 0)
    pwm_drive(pwm, STOP_PWM + control, 1)
