from rpi_hardware_pwm import HardwarePWM
import time

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


if __name__ == "__main__":

	pwm = pwm_init(46.7, 46.7)
	pwm_output(pwm, OFF_PWM, 1)
	pwm_output(pwm, OFF_PWM, 0)
	time.sleep(1)
	pwm_output(pwm, FORWARD_PWM, 1)
	pwm_output(pwm, FORWARD_PWM, 0)
	time.sleep(1)
	pwm_output(pwm, STOP_PWM, 1)
	pwm_output(pwm, STOP_PWM, 0)
	time.sleep(2)
	pwm_output(pwm, STOP_PWM + 0.5, 1)
	pwm_output(pwm, STOP_PWM - 0.5, 0)
	time.sleep(10)
	pwm_output(pwm, STOP_PWM, 1)
	pwm_output(pwm, STOP_PWM, 0)
