from rpi_hardware_pwm import HardwarePWM


# Duty cycle values
# PWM pins for default Device Tree Overlay is channel0 -> Pin 18
# channel1 -> Pin 19
backwards_pwm = 5
stop_pwm = 7.5
forward_pwm = 10
off_pwm = 0
pwm = HardwarePWM(pwm_channel=0, hz=50)
pwm.start(off_pwm)

def pwm_output(duty_cycle, finish_pwm=False):
   # pwm = HardwarePWM(pwm_channel=0, hz=50)
    pwm.stop()
    pwm.start(duty_cycle)
    #pwm.change_duty_cyle(10)

pwm_output(forward_pwm)
