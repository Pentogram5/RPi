from SC_infrared import *
import time

while True:
    print(RI_1.getSerialise(), RI_1.getNewValue())
    print(RI_2.getSerialise(), RI_1.getNewValue())
    print(RI_3.getSerialise(), RI_1.getNewValue())
    time.sleep(0.1)
