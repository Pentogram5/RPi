from SC_servo import *
import time
servo.set(1, 90)

S = ScServo()

while True:
    servo1, t, angle = map(int, input().split())
    state = {servo1: {'time': t, 'stopAngle': angle}}
    print(state)
    T = S.calcTrajectory(state)
    print(T)
    for i in T[1]:
        servo.set(servo1, i)
        time.sleep(1 / 5)

