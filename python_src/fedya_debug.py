from SC_servo import *
import time

S = ScServo()

while True:
    servo, t, angle = map(int, input().split())
    state = {servo: {'time': t, 'stopAngle': angle}}
    print(state)
    T = S.calcTrajectory(state)
    print(T)
    S.executeTrajectory(T)
    print(S.currentState)

