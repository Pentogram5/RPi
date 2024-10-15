from xr_servo import Servo
servo = Servo()

import numpy as np
import time


class ScServo:
    samplingRate = 1
    currentState = {1: 90,
                    2: 90,
                    3: 90,
                    4: 90,
                    5: 90,
                    6: 90
                    }
    expeditionState = {1: {'time': 1, 'stopAngle': 10}}

    # Рассчёт плавной траектории. Время траветории в секундах, начальный угол, конечный угол
    def calcSmothMove(self, time, startAngle, stopAngle):
        t = np.linspace(0, 1, self.samplingRate * time)
        bezier = t * t * (3 - 2 * t)
        angles = bezier * abs(stopAngle - startAngle)
        angles += startAngle if startAngle < stopAngle else stopAngle
        if not startAngle < stopAngle:
            angles = angles[::-1]
        angles = np.rint(angles).astype(int)
        return angles
    
    def calcTrajectory(self, endState):
        trajectory = endState.copy()
        for key in endState.keys():
            trajectory[key] = self.calcSmothMove(endState[key]['time'],
                                                 self.currentState[key],
                                                 endState[key]['stopAngle'])
        return trajectory
    
    def executeTrajectory(self, trajectory):
        count = 0
        f = True
        while f:
            f = False
            for key in trajectory.keys():
                if count < len(trajectory[key]):
                    angle = trajectory[key][count]
                    servo.set(key, angle)
                    print(key, angle)
                    f = True
                else:
                    self.currentState[key] = trajectory[key][-1]
            count += 1
            print(count)
            time.sleep(1 / self.samplingRate)
            