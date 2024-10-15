import time
class TimeStamper:
    def __init__(self):
        self.old_t = time.time()

    def timestamp(self):
        dt = time.time() - self.old_t
        self.old_t = time.time()
        return dt

ts = TimeStamper()

class RobotDirection:
    def __init__(self, left=1, right=1):
        self.speed_const_left = left
        self.speed_const_right = right
    def set_speed_cms_left(self, speed):
        print(speed, ts.timestamp())
        return speed
    def set_speed_cms_right(self, speed):
        return speed