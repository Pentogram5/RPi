from SC_servo import *
import time

S = ScServo()

while True:
    servo, t, angle = map(int, input().split())
    state = {servo: {'time': t, 'stopAngle': angle}}
    T = S.calcTrajectory(state)
    print(T)
    
