import os
import time

from xr_motor import RobotDirection
go = RobotDirection()

def setMotor(motor, direction, speed):
    go.set_speed(motor, speed * abs(direction - 1))
    if direction <= 1:
        if motor == 1:
            go.m1m2_forward()
        else:
            go.m3m4_forward()
    else:
        if motor == 1:
            go.m1m2_reverse()
        else:
            go.m3m4_reverse()


def setDirection(direction, speed):
    if direction == 0.0:
        setMotor(1, 0, speed)
        setMotor(2, 0, speed)
    elif direction > 0:
        setMotor(1, abs(direction), speed)
        setMotor(2, 0, speed)
    else:
        setMotor(1, 0, speed)
        setMotor(2, abs(direction), speed)

while True:
    try:
        direction, speed = map(float, input().split())
    except:
        go.stop()
    setDirection(direction, speed)