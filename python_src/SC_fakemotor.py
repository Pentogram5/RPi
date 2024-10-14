class RobotDirection:
    def __init__(self, left=1, right=1):
        self.speed_const_left = left
        self.speed_const_right = right
    def set_speed_cms_left(self, speed):
        return speed
    def set_speed_cms_right(self, speed):
        return speed