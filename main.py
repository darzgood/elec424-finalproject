from simple_pid import PID
import bno055_read
import sys
import time

# Index for IMU functions
select = 0

# Angle that we want the submersible to go to. Input from command line
desired_angle = (int(sys.argv[1]) + bno055_read.euler()[select]) % 360

# Set up pid to account for proportionality
#pid = PID(.1, 0.01, 0.005, setpoint=desired_angle)
pid = PID(.1, 0, 0, setpoint=desired_angle)

# Set min and max of PID output
pid.output_limits = (-2.5, 2.5)


# This whole code block makes all the angles positive in the range [0, 360]
if bno055_read.euler()[select] - desired_angle > 180:  # Finding diff between desired angle and measured
    offset = +180
elif bno055_read.euler()[select] - desired_angle < -180:  # Finding diff between desired angle and measured
    offset = -180
else:
    offset = 0

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

pwm = pwm_init(50, 50)  # Set pwm at 50 hz for each channel
#pwm_output(pwm, STOP_PWM, 1)
#pwm_output(pwm, BACK_PWM, 0)

# Assume we have a system we want to control in controlled_system
#v = controlled_system.update(0)
pwm_output(pwm, OFF_PWM, 0)  # Set each channel to off duty cycle
pwm_output(pwm, OFF_PWM, 1)

time.sleep(2)  # let motors set up

# Calibration for motors below
pwm_output(pwm, FORWARD_PWM, 0)  # Set each motor to full forward power
pwm_output(pwm, FORWARD_PWM, 1) 

time.sleep(2)  # let motors run

pwm_output(pwm, STOP_PWM, 0)  # Set each motor to stop mode 
pwm_output(pwm, STOP_PWM, 1)

time.sleep(2)  # Let motors set up

while True:
    # Compute new output from the PID according to the systems current value
    angle = bno055_read.euler()[select]  # Reading from IMU
    heading = bno055_read.mag()  # Reading from magnetometer

    if angle is None:  # sometimes angle is NoneType, so we continue so there is no bug
        continue
    if abs(angle - desired_angle) > 180:  # Add offset if the angle needs it
        angle += offset

    control = pid(angle)  # Outputs PWM value for motores
    print("Target: {}, \t Current: {}, \t PID: {}, \t Compass Heading: {}".format(round(desired_angle,2), round(angle,2), round(control,2), heading))

#    if (control > FORWARD_PWM - STOP_PWM):
#	control = FORWARD_PWM - STOP_PWM
#    else if (control < -2.5):
#	control = -2.5


    # Feed the PID output to the system and get its current value
    #    v = controlled_system.update(control)
    pwm_output(pwm, STOP_PWM + control, 0)  # Adjust PWM based on sensor
    pwm_output(pwm, STOP_PWM - control, 1)
