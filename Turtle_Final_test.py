from lx16a import *
from math import sin,cos
import time
import pandas as pd
import numpy as np

#pd.set_option('display.max_columns',1000)

LX16A.initialize("/dev/ttyUSB0")

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

## Moving Motors to Starting Position

RR_calf_init = 140;RR_leg_init = 90;FR_calf_init = 155;FR_leg_init = 75
RL_calf_init=90;RL_leg_init = 140;FL_calf_init=90;FL_leg_init = 140

RR_calf.move(RR_calf_init);RR_leg.move(RR_leg_init)
FR_calf.move(FR_calf_init);FR_leg.move(FR_leg_init)
RL_calf.move(RL_calf_init);RL_leg.move(RL_leg_init)
FL_calf.move(FL_calf_init);FL_leg.move(FL_leg_init)

time.sleep(2)

# Initial Parameter Identification
temp_array = np.transpose([RR_calf.get_temp(),RL_calf.get_temp(),FL_calf.get_temp(),FR_calf.get_temp(),RR_leg.get_temp(),RL_leg.get_temp(),FL_leg.get_temp(),FR_leg.get_temp()])
vin_array = np.transpose([RR_calf.get_vin(),RL_calf.get_vin(),FL_calf.get_vin(),FR_calf.get_vin(),RR_leg.get_vin(),RL_leg.get_vin(),FL_leg.get_vin(),FR_leg.get_vin()])
real_phys_pos = np.transpose([RR_calf.get_physical_angle(),RL_calf.get_physical_angle(),FL_calf.get_physical_angle(),FR_calf.get_physical_angle(),RR_leg.get_physical_angle(),RL_leg.get_physical_angle(),FL_leg.get_physical_angle(),FR_leg.get_physical_angle()])
theor_pos = np.transpose([RR_calf_init,RL_calf_init,FL_calf_init,FR_calf_init,RR_leg_init,RL_leg_init,FL_leg_init,FR_leg_init])
stdev = 10 # allowed deviation between motor positions
t_max = 60 # maximum allowed temperature
v_min = 4 # minimum acceptable voltage


## Checking Initial Motor Temperature, Voltage and Position
cols = ["RR_calf","RL_calf","FL_calf","FR_calf","RR_leg","RL_leg","FL_leg","FR_leg"]
temp_vol_pos = [[RR_calf.get_temp(),RL_calf.get_temp(),FL_calf.get_temp(),FR_calf.get_temp(),RR_leg.get_temp(),RL_leg.get_temp(),FL_leg.get_temp(),FR_leg.get_temp()],[RR_calf.get_vin(),RL_calf.get_vin(),FL_calf.get_vin(),FR_calf.get_vin(),RR_leg.get_vin(),RL_leg.get_vin(),FL_leg.get_vin(),FR_leg.get_vin()],[RR_calf.get_physical_angle(),RL_calf.get_physical_angle(),FL_calf.get_physical_angle(),FR_calf.get_physical_angle(),RR_leg.get_physical_angle(),RL_leg.get_physical_angle(),FL_leg.get_physical_angle(),FR_leg.get_physical_angle()],[RR_calf_init,RL_calf_init,FL_calf_init,FR_calf_init,RR_leg_init,RL_leg_init,FL_leg_init,FR_leg_init]]
index = ['Temperature (Celsius)','Input Voltage (mV)','Motor Position (degrees)','Theoretical Motor Position (degrees)']
df = pd.DataFrame(data=temp_vol_pos,columns = cols, index = index)
print("\nThe initial values for robot parameters are listed below \n")
print(df.to_string())

# Temp Validation
for i in range(len(temp_array)):
   if t_max <= temp_array[i]:
      print(f"Motor {i+1} is overheating, please let it cool. The program will exit now.")
      exit()

# Voltage Validation
for i in range(len(vin_array)):
   if vin_array[i] <= v_min:
      print(f"The input voltage to motor {i+1} is insufficient. Please charge the power bank. The program will exit now.")
      exit()

# Motor Position Validation
for i in range(len(real_phys_pos)):
   if real_phys_pos[i] <= theor_pos[i]-stdev or real_phys_pos[i] >= theor_pos[i]+stdev:
      print(f"The initialized position of motor {i+1} does not match the defined value. Please check the status of the motor. The program will exit now.")
      exit()

time.sleep(2) # Wait time to ensure that the motors are at the correct starting position

## Movement Section

ang = 15
t = 0
a = 1

def motorparam(num):
   if num % 50 == 0:
      print("\nThe current robot parameters at t =",num/10,"are listed below. \n")
      print(df)
while t < 30:
    RR_calf.move((-cos(t)*ang + RR_calf_init))
    FL_calf.move((cos(t)*ang + FL_calf_init))
    RR_leg.move((-sin(t)*ang + RR_leg_init))
    FL_leg.move((sin(t)*ang + FL_leg_init))
    #print("HI")
    time.sleep(0.05)  
    RL_calf.move((-cos(t)*ang + RL_calf_init))
    FR_calf.move((cos(t)*ang + FR_calf_init))
    RL_leg.move((-sin(t)*ang + RL_leg_init))
    FR_leg.move((sin(t)*ang + FR_leg_init))
    time.sleep(0.05)

    for i in range(len(temp_array)):
       if t_max <= temp_array[i]:
          print(f"Motor {i+1} is overheating, please let it cool. The program will exit now.")
          exit()
    for i in range(len(vin_array)):
       if vin_array[i] <= v_min:
          print(f"The input voltage to motor {i+1} is insufficient. Please charge the power bank. The program will exit now.")
          exit()
    for i in range(len(real_phys_pos)):
       if real_phys_pos[i] <= theor_pos[i]-stdev or real_phys_pos[i] >= theor_pos[i]+stdev:
          print(f"The initialized position of motor {i+1} does not match the defined value. Please check the status of the motor. The program will exit now.")
          exit()
    motorparam(a)
    t += 0.1
    a += 1
time.sleep(2)

## Moving to Resting Position

RR_calf_init = 165;RR_leg_init = 45;FR_calf_init = 180;FR_leg_init = 30
RL_calf_init=65;RL_leg_init = 180;FL_calf_init=65;FL_leg_init = 180

RR_calf.move(RR_calf_init);time.sleep(0.05);RR_leg.move(RR_leg_init);time.sleep(0.05)
FR_calf.move(FR_calf_init);time.sleep(0.05);FR_leg.move(FR_leg_init);time.sleep(0.05);
RL_calf.move(RL_calf_init);time.sleep(0.05);RL_leg.move(RL_leg_init);time.sleep(0.05)
FL_calf.move(FL_calf_init);time.sleep(0.05);FL_leg.move(FL_leg_init)

df = pd.DataFrame(data=temp_vol_pos,columns = cols, index = index)
print("\nThe final values for robot parameters are listed below \n")
print(df.to_string())

# Motor End-Position Validation
for i in range(len(real_phys_pos)):
   if real_phys_pos[i] <= theor_pos[i]-stdev or real_phys_pos[i] >= theor_pos[i]+stdev:
      print(f"\nThe final position of motor {i+1} does not match the defined value. Please check the status of the motor. The program will exit now.")
      exit()
