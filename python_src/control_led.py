from xr_car_light import Car_light

import time

def red_light(Car_light):
    Car_light.set_ledgroup(2, 8, 1)
    
def green_light(Car_light):
    Car_light.set_ledgroup( 2, 8, 4)
    
cl = Car_light()
while True:
    red_light(cl)
    time.sleep(2)
    green_light(cl)