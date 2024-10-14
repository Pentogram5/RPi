from SC_infrared import *
import time

while True:
    print(IR_1.getSerialise(), IR_1.getNewValue())
    print(IR_2.getSerialise(), IR_1.getNewValue())
    print(IR_3.getSerialise(), IR_1.getNewValue())
    time.sleep(0.1)
