import pwm_test
import pigpio
import time


hardwarePin = 18
BACK_PWM = 5
STOP_PWM = 7.5
FORWARD_PWM = 10
OFF_PWM = 0
# import os     #importing os library so as to communicate with the system
# os.system ("sudo pigpiod") #Launching GPIO library

class Motor:
    def __init__(self, pi=pigpio.pi(), pin=18, direction = 1, max_pos = 2300, min_pos=1000):
        self.pin = pin
        self.max_pos = max_pos
        self.min_pos = min_pos
        self.dir = direction
        self.pi = pi
        self.current_pos = 0
        self.pwm = None
        pi.set_mode(pin, pigpio.OUTPUT)
        self.pwm_flag = False

    def pwm_init(self, freq1, freq2):
        self.pwm = pwm_test.pwm_init(freq1, freq2)
        self.pwm_flag = True

    def pwm_output(self, dut, chan):
        if self.pwm_flag and (chan == 0 or chan == 1):
            pwm_test.pwm_output(self.pwm, dut, chan)

    def test(self):
        # Could run PID_step_test here
        for i in range(self.min_pos, self.max_pos, 1):
            self.pi.set_servo_pulsewidth(self.pin, i);
        for i in range(self.max_pos, self.min_pos, -1):
            self.pi.set_servo_pulsewidth(self.pin, i);
        self.stop()

    def stop(self):
        self.pi.set_servo_pulsewidth(self.pin, 0)

    def fd(self):
        self.pi.set_servo_pulsewidth(self.pin, self.max_pos)

    def bk(self):
        self.pi.set_servo_pulsewidth(self.pin, self.min_pos)

# Not used for this project

class Servo(Motor):
#   def __init__(self, pi, pin, direction = 1, max_pos = 2300, min_pos=1000):
#     super().__init__(self, pi, pin, direction, max_pos, min_pos)
  def goToAngle(self, angle):
    ticks_per_angle = (self.max_pos - self.min_pos)/180 
    if (0 < angle < 180):
      self.pi.set_servo_pulsewidth(self.pin, ticks_per_angle*angle)

class BrushlessDC(Motor):
  def __init__(self, pi, pin, direction=1, max_pos=2500, min_pos=500):
    super().__init__(pi, pin, direction, max_pos, min_pos)


  def arm(self):
    self.pi.set_servo_pulsewidth(self.pin, 0)
    time.sleep(1)
    self.pi.set_servo_pulsewidth(self.pin, self.max_pos)
    time.sleep(1)
    self.pi.set_servo_pulsewidth(self.pin, self.min_pos)
    time.sleep(1)

  def drive(self, speed = 0):
    ticks = 1500 + speed
    self.pi.set_servo_pulsewidth(self.pin, ticks)

  def calibrate(self):
    self.pi.set_servo_pulsewidth(self.pin, 0)
    print("Disconnect the battery and press Enter")
    inp = input()
    if inp == '':
        self.pi.set_servo_pulsewidth(self.pin, self.max_pos)
        print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        inp = input()
        if inp == '':            
            self.pi.set_servo_pulsewidth(self.pin, self.min_pos)
            print("Wierd eh! Special tone")
            time.sleep(7)
            print("Wait for it ....")
            time.sleep (5)
            print("Im working on it, DONT WORRY JUST WAIT.....")
            self.pi.set_servo_pulsewidth(self.pin, 0)
            time.sleep(2)
            print("Arming ESC now...")
            self.pi.set_servo_pulsewidth(self.pin, self.min_pos)
            time.sleep(1)
            print("See.... uhhhhh")

if __name__ == '__main__':
    pi = pigpio.pi()
    ballast = Motor(pi, ballastPin)
    ballast.test()
    pi.stop()
