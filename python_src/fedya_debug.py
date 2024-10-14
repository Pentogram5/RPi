import SC_infrared as I
import time

I1 = I.ScInfrared(1, 18, 100) 
while True:
    print(I1.getNewRawValue())
    time.sleep(0.1)
