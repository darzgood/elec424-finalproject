### Submersible heading control ###
# Darrell Good, John Reko, Ryan Pai, Sean Hamilton
# Rice University - ELEC 424
# 12-8-2023

from simple_pid import PID
import bno055_read
import sys
import time
import atexit

# Index for IMU functions
select = 0

# Angle that we want the submersible to go to. Input from command line
desired_angle = (int(sys.argv[1]) + bno055_read.euler()[select]) % 360

# Set up pid controller
# Contants initially determined with the Ziegler–Nichols method, and then manually adjusted
pid = PID(.02, 0, .004, setpoint=desired_angle)

# Cap the pid output so that the pwm duty cycle does not exceed the motors operational limits
pid.output_limits = (-0.5, 0.5)

# Import hardware PWM class
from rpi_hardware_pwm import HardwarePWM


# PWM pins for default Device Tree Overlay is channel0 -> Pin 18
# channel1 -> Pin 13

# Duty cycle constants (in %)
BACK_PWM = 5
STOP_PWM = 7.5
FORWARD_PWM = 10
OFF_PWM = 0

# 50hz is the nominal frequency for servo and brushless drives, 
# but hardware variations result in this value needing to be adjusted
PWM_FREQ = 46.7; 

def pwm_init(frequency1, frequency2):
    '''Initializes both channels of the hardware pwm generator.
    Args: 
      frequency1: frequency to assign to pwm channel 0 (int)
      frequency2: frequency to assign to pwm channel 1 (int)

    Returns:
      Tuple containing hardware pwm objects for both channels
    '''
    pwm0 = HardwarePWM(pwm_channel=0, hz=frequency1)  # Set pwm channel 0 
    pwm1 = HardwarePWM(pwm_channel=1, hz=frequency2)  # set pwm channel 1
    pwm = (pwm0, pwm1)  # Put in tuple to have access to both with the output
    pwm[0].start(OFF_PWM)  # Start each channel at OFF duty cycle for motors
    pwm[1].start(OFF_PWM)
    return pwm

def pwm_output(pwm_channels, duty_cycle, channel):
    '''Starts a pwm channel at a new duty cycle.
    Args: 
      pwm_channels: Tuple of pwm channels.
      duty_cycle:   Duty cycle to set to (%) 
      channel:      Channel to modify

    Returns:
      0 if successful
    '''
    # Note that pwm input is a tuple of both pwm channel
    pwm_channels[channel].stop()  # Stop whatever pwm channel duty cycle was occurring
    pwm_channels[channel].start(duty_cycle)  # REset duty cycle to input
    return 0

def pwm_drive(pwm_channels, duty_cycle, channel):
    '''Modifies an already running pwm channel by adjusting the duty cycle.
    Args: 
      pwm_channels: Tuple of pwm channels.
      duty_cycle:   Duty cycle to set to (%) 
      channel:      Channel to modify

    Returns:
      0 if successful
    '''
    pwm_channels[channel].change_duty_cycle(duty_cycle)
    return 0

def arm_motors(pwm):
    '''Runs through the startup sequence for Diamond Dynamics TD1.2 motors (and
        many other brushless DC motors). This must be called once on powerup.

    Args: 
      pwm_channels: Tuple of pwm channels connected to thrusters.

    Returns:
      None
    '''

    # Turn motor off for 1 sec
    pwm_output(pwm, OFF_PWM, 1)
    pwm_output(pwm, OFF_PWM, 0)
    time.sleep(1)

    # Give motor full power signal for 1 sec
    pwm_output(pwm, FORWARD_PWM, 1)
    pwm_output(pwm, FORWARD_PWM, 0)
    time.sleep(1)

    # Return motor to nuetral state
    pwm_output(pwm, STOP_PWM, 1)
    pwm_output(pwm, STOP_PWM, 0)
    time.sleep(1)

def wrap_angle(angle, desired):
    '''Calculates the offset for the current angle to compensate for mod-360 
      effects 

    Args: 
      angle:   current angle of the submersible
      desired: target angle of the submerisble

    Returns:
      One of {0, 360, -360} corresponding to the appropriate angle offset
    '''
    if angle - desired > 180:
        offset = -360    
    elif angle - desired < -180:
        offset = +360
    else:
        offset = 0
    return offset

# Create the hardware pwm objects and run through the initialization and arming sequences.
pwm = pwm_init(PWM_FREQ, PWM_FREQ)
arm_motors(pwm)

def exit_handler():
    """ Kills motors on program exit"""
    pwm[0].stop()
    pwm[1].stop()

# Register the exit handler so that CTRL+C kills both the program and the motors.
atexit.register(exit_handler)
time.sleep(2)


vals = [] # Averaging array
while True:
    # Compute new output from the PID according to the systems current value
    angle = bno055_read.euler()[select]  # Reading from IMU
    heading = bno055_read.mag()  # Reading from magnetometer

    if angle is None:  # Skip the reading if the IMU returns a NoneType
        continue
    if not (0 <= angle <= 360): #Skip out-of-bounds IMU readings
        continue

    # Adjust the reading to garauntee that the sub takes the 
    # shortest route to the desired angle
    angle += wrap_angle(angle, desired_angle) 

    # Average out 10 readings to increase stability
    vals.append(angle)
    if len(vals) < 10:
        continue
    else:
        angle = sum(vals)/len(vals)
        vals = []

    # Use PID to calculate the PWM value for motors
    control = pid(angle)  

    # Feed the PID output to the system.
    # Motors are turned opposite directions so that the sub turns
    pwm_drive(pwm, STOP_PWM - control, 0)  
    pwm_drive(pwm, STOP_PWM + control, 1)

    # Debug and info to terminal
    print("Target: {}, \t Current: {}, \t PID: {}, \t Compass Heading: {}".format(round(desired_angle,2), round(angle,2), round(control,2), heading))

