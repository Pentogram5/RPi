"""
树莓派WiFi无线视频小车机器人驱动源码
作者：Sence
版权所有：小R科技（深圳市小二极客科技有限公司www.xiao-r.com）；WIFI机器人网论坛 www.wifi-robots.com
本代码可以自由修改，但禁止用作商业盈利目的！
本代码已申请软件著作权保护，如有侵权一经发现立即起诉！
"""
"""
@version: python3.7
@Author  : xiaor
@Explain :电机控制
@contact :
@Time    :2020/05/09
@File    :xr_motor.py
@Software: PyCharm
"""
from builtins import float, object

import os
import threading
import xr_gpio as gpio
import xr_config as cfg
import time

from xr_configparser import HandleConfig
path_data = os.path.dirname(os.path.realpath(__file__)) + '/data.ini'
cfgparser = HandleConfig(path_data)

def sleep_duty_cycle(T, duty):
    time.sleep(T*duty)

def sleep_free_cycle(T, duty):
    time.sleep(T*(1-duty))
    
def sgn(x):
    """Return the sign of a float.
    
    Args:
        x (float): The input number.

    Returns:
        int: -1 if x is negative, 1 if x is positive, 0 if x is zero.
    """
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

class RobotDirection(object):

    def __init__(self, fps=3):
        self.min_speed_out = 10
        self.min_speed_in  = 20
        self.base_speed = 100
        self.k_low_pwm = 7
        self.T = 1/fps
        self.advanced_speed_left = 0
        self.advanced_movement_left  = False
        
        self.advanced_speed_right = 0
        self.advanced_movement_right = False
        self.start_processing_low_speeds()
        
        self.speed_const_left = 1
        self.speed_const_right = 1
        self.a = 0.37
        self.b = 9

    def set_consts(self,left,right):
        self.speed_const_left = left
        self.speed_const_right = right
    
    def start_processing_low_speeds(self):
        self.th = threading.Thread(target=self._process_low_speeds_left)
        self.th.start()
        self.th = threading.Thread(target=self._process_low_speeds_right)
        self.th.start()
    
    def get_duty_cycle(self, speed):
        # print(self.__dir__())
        s_in_abs  = abs(speed) * self.k_low_pwm
        k_out = self.min_speed_out / self.min_speed_in # from in to out
        s_out = s_in_abs * k_out
        cycle = s_out / self.base_speed
        return min(cycle, 1)
    
    def _process_low_speeds_left(self):
        while True:
            if self.advanced_movement_left:
                s = self.advanced_speed_left
                flag = sgn(s)
                speed_in = abs(s)
                duty = self.get_duty_cycle(speed_in)
                
                # print(speed_in, duty)
                self._set_speed_left(flag, self.base_speed)
                sleep_duty_cycle(self.T, duty)
                self._set_speed_left(0, 0)
                sleep_free_cycle(self.T, duty)
            else:
                time.sleep(self.T*2)
    
    def _process_low_speeds_right(self):
        while True:
            if self.advanced_movement_right:
                s = self.advanced_speed_right
                flag = sgn(s)
                speed = abs(s)
                duty = self.get_duty_cycle(speed)
                # print(speed, duty)
                
                self._set_speed_right(flag, self.base_speed)
                sleep_duty_cycle(self.T, duty)
                self._set_speed_right(0, 0)
                sleep_free_cycle(self.T, duty)
            else:
                time.sleep(self.T*2)
    
    def get_out_speed(self, cms):
        cms_abs = abs(cms)
        cms_sgn = sgn(cms)
        speed = cms_abs*self.speed_const_left
        speed = round((speed-self.b)/self.a)
        return cms_sgn, speed
        
    #МАКСИМАЛЬНАЯ СКОРОСТЬ 46 МИН/С	(self.a*100 + self.b)
    #МИНИМАЛЬНАЯ СКОРОСТЬ  10 МИН/С (self.b+1)
    def preprocess_speed(self, speed):
        fl_advanced = False
        flag = 0
        # print(self.__dir__())
        if ( (abs(speed)<=self.min_speed_in) and (abs(speed)>0) ):
            fl_advanced = True
            # flag, speed = speed
            # speed = self.b
            # flag = 0
            return flag, speed, fl_advanced
        
        flag, speed = self.get_out_speed(speed)
        
        
        if speed > 100: speed = 100
        if speed < 0: speed = 0 
        return flag, speed, fl_advanced

    def _set_speed_left(self, flag, speed):
        if (flag > 0):
            self.m1m2_forward()
            gpio.ena_pwm(speed)
        elif (flag == 0):
            self.m1m2_stop()
        else:
            self.m1m2_reverse()
            gpio.ena_pwm(speed)
    
    def _set_speed_right(self, flag, speed):
        # print(speed)
        if (flag > 0):
            self.m3m4_forward()
            gpio.enb_pwm(speed)
        elif (flag == 0):
            self.m3m4_stop()
        else:
            self.m3m4_reverse()
            gpio.enb_pwm(speed)
    
    def set_speed_cms_left(self,speed):
        # Если не нужно спец движений - устанавливает текущую скорость
        flag, self.advanced_speed_left, self.advanced_movement_left = self.preprocess_speed(speed)
        # print(flag, self.advanced_speed_left, self.advanced_movement_left)
        if not self.advanced_movement_left:
            self._set_speed_left(flag, self.advanced_speed_left)
        
    
    def set_speed_cms_right(self,speed):
        # print(speed)
        flag, self.advanced_speed_right, self.advanced_movement_right = self.preprocess_speed(speed)
        if not self.advanced_movement_right:
            self._set_speed_right(flag, self.advanced_speed_right)
        

    def set_speed(self, num, speed):
        """
        设置电机速度，num表示左侧还是右侧，等于1表示左侧，等于右侧，speed表示设定的速度值（0-100）
        """
        # print(speed)
        if num == 1:  # 调节左侧
            gpio.ena_pwm(speed)
        elif num == 2:  # 调节右侧
            gpio.enb_pwm(speed)

    def motor_init(self):
        """
        Получите скорость хранения данных роботом
        """
        print("Получите скорость хранения данных роботом")
        speed = cfgparser.get_data('motor', 'speed')
        cfg.LEFT_SPEED = speed[0]
        cfg.RIGHT_SPEED = speed[1]
        print(speed[0])
        print(speed[1])

    def save_speed(self):
        speed = [0, 0]
        speed[0] = cfg.LEFT_SPEED
        speed[1] = cfg.RIGHT_SPEED
        cfgparser.save_data('motor', 'speed', speed)

    def m1m2_forward(self):
        # 设置电机组M1、M2正转
        gpio.digital_write(gpio.IN1, True)
        gpio.digital_write(gpio.IN2, False)

    def m1m2_reverse(self):
        # 设置电机组M1、M2反转
        gpio.digital_write(gpio.IN1, False)
        gpio.digital_write(gpio.IN2, True)

    def m1m2_stop(self):
        # 设置电机组M1、M2停止
        gpio.digital_write(gpio.IN1, False)
        gpio.digital_write(gpio.IN2, False)

    def m3m4_forward(self):
        # 设置电机组M3、M4正转
        gpio.digital_write(gpio.IN3, True)
        gpio.digital_write(gpio.IN4, False)

    def m3m4_reverse(self):
        # 设置电机组M3、M4反转
        gpio.digital_write(gpio.IN3, False)
        gpio.digital_write(gpio.IN4, True)

    def m3m4_stop(self):
        # 设置电机组M3、M4停止
        gpio.digital_write(gpio.IN3, False)
        gpio.digital_write(gpio.IN4, False)

    def forward(self):
        """
        设置机器人运动方向为前进
        """
        self.set_speed(1, cfg.LEFT_SPEED)
        self.set_speed(2, cfg.RIGHT_SPEED)
        self.m1m2_forward()
        self.m3m4_forward()

    def back(self):
        """
        #设置机器人运动方向为后退
        """
        self.set_speed(1, cfg.LEFT_SPEED)
        self.set_speed(2, cfg.RIGHT_SPEED)
        self.m1m2_reverse()
        self.m3m4_reverse()

    def left(self):
        """
        #设置机器人运动方向为左转
        """
        self.set_speed(1, cfg.LEFT_SPEED)
        self.set_speed(2, cfg.RIGHT_SPEED)
        self.m1m2_reverse()
        self.m3m4_forward()

    def right(self):
        """
        #设置机器人运动方向为右转
        """
        self.set_speed(1, cfg.LEFT_SPEED)
        self.set_speed(2, cfg.RIGHT_SPEED)
        self.m1m2_forward()
        self.m3m4_reverse()

    def stop(self):
        """
        #设置机器人运动方向为停止
        """
        self.set_speed(1, 0)
        self.set_speed(2, 0)
        self.m1m2_stop()
        self.m3m4_stop()
