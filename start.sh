#!/bin/sh

sleep 30
git pull origin main
sleep 7
sudo python /home/pi/work/python_src/xr_startmain.py &
sleep 5
sudo node /home/pi/work/XiaoRGeekBle/code/XiaoRGeek/main.js &
exit 0



