from simple_pid import PID
import bno055_read
import sys

desired_angle = (sys.argv[0] + bno055_read.euler()[2]) % 360

pid = PID(1, 0.1, 0.05, setpoint=desired_angle)

select = 0

if bno055_read.euler()[select] - desired_angle > 180:
    offset = +180
elif bno055_read.euler()[select] - desired_angle < -180:
    offset = -180
else:
    offset = 0

# Assume we have a system we want to control in controlled_system
v = controlled_system.update(0)

while True:
    # Compute new output from the PID according to the systems current value
    angle = euler()[select]

    if abs(angle - desired_angle) > 180:
        angle += offset

    control = pid(v)

    # Feed the PID output to the system and get its current value
    v = controlled_system.update(control)

