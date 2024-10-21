from xr_car_light import Car_light

import time

car_light = Car_light()
def red_light():
    global car_light
    car_light.set_ledgroup(1, 8, 1)
    car_light.set_ledgroup(2, 8, 1)
    
def green_light():
    global car_light
    car_light.set_ledgroup(1, 8, 4)
    car_light.set_ledgroup(2, 8, 4)

def off_led():
    global car_light
    car_light.set_ledgroup(1, 8, 0)
    car_light.set_ledgroup(2, 8, 0)
if __name__=='__main__':
    while True:
        red_light()
        time.sleep(2)
        green_light()
        time.sleep(2)