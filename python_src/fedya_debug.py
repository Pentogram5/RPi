from SC_servo import *
import time
servo.set(1, 90)

S = ScServo()

while True:
    d, servo1, t, angle = map(int, input().split())
    begintime = time.time()
    S.samplingRate = d
    state = {servo1: {'time': t, 'stopAngle': angle}}
    print(state)
    T = S.calcTrajectory(state)
    print(T)
    S.executeTrajectory(T)
    print(S.currentState)
    print(time.time() - begintime)

