from xr_servo import Servo
servo = Servo()

import smbus
SM = smbus.SMBus(1)

import numpy as np
import time


class ScServo:
    samplingRate = 50
    currentState = {1: 90,
                    2: 90,
                    3: 90,
                    4: 90,
                    5: 90,
                    6: 90
                    }
    expeditionState = {1: {'time': 0.5, 'stopAngle': 150},
                       2: {'time': 0.75, 'stopAngle': 35},
                       3: {'time': 0.5, 'stopAngle': 95},
                       4: {'time': 0.5, 'stopAngle': 100}}
    catchState = {1: {'time': 0.7, 'stopAngle': 4},
                  2: {'time': 0.35, 'stopAngle': 185},
                  3: {'time': 0.5, 'stopAngle': 95},
                  4: {'time': 0.25, 'stopAngle': 50}}
    putState = {1: {'time': 0.7, 'stopAngle': 70},
                  2: {'time': 0.35, 'stopAngle': 100},
                  3: {'time': 0.5, 'stopAngle': 95}}
    catch = {4: {'time': 0.25, 'stopAngle': 100}}
    throw = {4: {'time': 0.25, 'stopAngle': 50}}

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
                    print(int(key))
                    angle = trajectory[key][count]
                    print(int(angle))
                    self.send(int(key), int(angle))
                    f = True
                else:
                    self.currentState[key] = trajectory[key][-1]
            count += 1
            time.sleep(1 / self.samplingRate)
    
    def send(self, servo, angle):
        values = [0xff, 0x01, servo, angle, 0xff]
        SM.write_i2c_block_data(0x18, values[0], values[1:len(values)])