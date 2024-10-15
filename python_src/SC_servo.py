from xr_servo import Servo
servo = Servo()

import numpy as np
import time


class ScServo:
    samplingRate = 100
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
            trajectory[key] = self.calcSmothMove(self.expeditionState[key]['time'],
                                                 self.currentState[key],
                                                 self.expeditionState[key]['stopAngle'])
        return trajectory
    
    def executeTrajectory(self, trajectory):
        count = 0
        while True:
            for key in trajectory.keys():
                if trajectory[key] != None:
                    try:
                        angle = trajectory[key][count]
                        servo.set(key, angle)
                    except:
                        trajectory[key] = None
                    count += 1
                    break
            else:
                break
            time.sleep(1 / self.samplingRate)