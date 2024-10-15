from xr_servo import Servo
servo = Servo()

class ScServo:
    samplingRate = 100
    def smoothlyMove(self, time, startAngle, stopAngle):
        return list(range(startAngle, stopAngle, self.samplingRate * time))
    def transportMode(self):
