import SC_infrared as I
import time

I1 = I.ScInfrared(1, 18) 
while True:
    print(I1.getNewValue())
    time.sleep(0.1)
