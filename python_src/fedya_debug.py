from SC_servo import *
import time

S = ScServo()

'''
while True:
    d, servo1, t, angle = map(float, input().split())
    d = int(d)
    servo1 = int(servo1)
    angle = int(angle)
    begintime = time.time()
    S.samplingRate = d
    state = {servo1: {'time': t, 'stopAngle': angle}}
    print(state)
    T = S.calcTrajectory(state)
    print(T)
    S.executeTrajectory(T)
    print(S.currentState)
    print(time.time() - begintime)

'''

while True:
    inp = input()
    if inp == 'c':
        S.executeTrajectory(S.calcTrajectory(S.catchState))
    elif inp == 'e':
        S.executeTrajectory(S.calcTrajectory(S.expeditionState))
    elif inp == 'set c':
        while True:
            n, t = int(input()), float(input())
            if n == 0:
                break
            S.catchState[n]['time'] = t
    elif inp == 'set e':
        while True:
            n, t = int(input()), float(input())
            if n == 0:
                break
            S.expeditionState[n]['time'] = t
    else:
        break