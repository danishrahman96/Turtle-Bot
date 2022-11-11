from lx16a import *
# from pylx16a.lx16a import *
from math import sin,cos
# import numpy as np
# import pandas as pd
import time
# import platform
# import sys


# initial position (vertical)
#1 - 110
# 2,3,4,8 are at 120
#5,6,7 are at 100

LX16A.initialize("COM1")

## Initializing and Defining Motors
try:
    RR_calf = LX16A(1)
    RL_calf = LX16A(2)
    FL_calf = LX16A(3)
    FR_calf = LX16A(4)
    RR_leg = LX16A(5)
    RL_leg = LX16A(6)
    FL_leg = LX16A(7)
    FR_leg = LX16A(8)

except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. The program will exit now.")
    exit()

# Moving Motors to Resting Position

RR_calf_init = 140;RR_leg_init = 90;FR_calf_init = 155;FR_leg_init = 75
RL_calf_init=90;RL_leg_init = 140;FL_calf_init=90;FL_leg_init = 140

RR_calf.move(RR_calf_init);RR_leg.move(RR_leg_init)
FR_calf.move(FR_calf_init);FR_leg.move(FR_leg_init)
RL_calf.move(RL_calf_init);RL_leg.move(RL_leg_init)
FL_calf.move(FL_calf_init);FL_leg.move(FL_leg_init)

time.sleep(2) # Wait time to ensure that the motors are at the correct starting position
# # headers = ['FR_thigh(1)','FR_calf (2)','FL_thigh (3)','FL_calf (4)','RR_thigh (5)','RR_calf (6)','RL_thigh (7)',
# # 'RR_calf (6)']


# #Checking Initial Angles in Array
# # init_arr = [FR_thigh.get_physical_angle(),FR_calf.get_physical_angle(),FL_thigh.get_physical_angle(),FL_calf.get_physical_angle(),
# #             RR_thigh.get_physical_angle(),RR_calf.get_physical_angle(),RL_thigh.get_physical_angle(),RL_calf.get_physical_angle()]
# # init_pos = [[headers[i]]+init_arr[i] for i in range(l+1)]


ang = 20
t = 0
while t < 10:
    RR_calf.move(cos(t)*ang+RR_calf_init)
    RR_leg.move(sin(t)*ang+RR_leg_init)
    FR_calf.move(sin(t)*ang+FR_calf_init)
    FR_leg.move(cos(t)*ang+FR_leg_init)
    RL_calf.move(sin(t)*ang+RL_calf_init)
    RL_leg.move(cos(t)*ang+RL_leg_init)
    FL_calf.move(cos(t)*ang+FL_calf_init)
    FL_leg.move(sin(t)*ang+FL_leg_init)
    
    time.sleep(0.05)

    t += 0.1

time.sleep(2)

#Moving to resting position
RR_calf_init = 165;RR_leg_init = 45;FR_calf_init = 180;FR_leg_init = 30
RL_calf_init=65;RL_leg_init = 180;FL_calf_init=65;FL_leg_init = 180

RR_calf.move(RR_calf_init)
time.sleep(0.05)
RR_leg.move(RR_leg_init)
time.sleep(0.05)
FR_calf.move(FR_calf_init)
time.sleep(0.05)
FR_leg.move(FR_leg_init)
time.sleep(0.05)
RL_calf.move(RL_calf_init)
RL_leg.move(RL_leg_init)
FL_calf.move(FL_calf_init)
FL_leg.move(FL_leg_init)