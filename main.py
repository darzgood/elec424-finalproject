from simple_pid import PID
import bno055_read
import sys
import time
import atexit



# Index for IMU functions
select = 0

# Angle that we want the submersible to go to. Input from command line
desired_angle = (int(sys.argv[1]) + bno055_read.euler()[select]) % 360

# Set up pid to account for proportionality
#pid = PID(.1, 0.01, 0.005, setpoint=desired_angle)
pid = PID(.02, 0, .004, setpoint=desired_angle)

pid.output_limits = (-0.5, 0.5)

# Import hardware PWM class
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
    pwm0 = HardwarePWM(pwm_channel=0, hz=frequency1)  # Set pwm channel 0 
    pwm1 = HardwarePWM(pwm_channel=1, hz=frequency2)  # set pwm channel 1
    pwm = (pwm0, pwm1)  # Put in tuple to have access to both with the output
    pwm[0].start(OFF_PWM)  # Start each channel at OFF duty cycle for motors
    pwm[1].start(OFF_PWM)
    return pwm

def pwm_output(pwm_channels, duty_cycle, channel):
    # Note that pwm input is a tupe with each pwm channel
    pwm_channels[channel].stop()  # Stop whatever pwm channel duty cycle was occurring
    pwm_channels[channel].start(duty_cycle)  # REset duty cycle to input
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

time.sleep(2)
vals = []
while True:
    # Compute new output from the PID according to the systems current value
    angle = bno055_read.euler()[select]  # Reading from IMU
    heading = bno055_read.mag()  # Reading from magnetometer

    if angle is None:  # sometimes angle is NoneType, so we continue so there is no bug
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

    control = pid(angle)  # Outputs PWM value for motores
    print("Target: {}, \t Current: {}, \t PID: {}, \t Compass Heading: {}".format(round(desired_angle,2), round(angle,2), round(control,2), heading))

    # Feed the PID output to the system and get its current value
    #    v = controlled_system.update(control)
    pwm_drive(pwm, STOP_PWM - control, 0)  # Adjust PWM based on sensor
    pwm_drive(pwm, STOP_PWM + control, 1)
