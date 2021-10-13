import numpy as np 
import matplotlib.pyplot as plt


max_h = 6.5         #max height of tank, m 
tank_dia = 31.3     #diamter of tank, m
initial_h = 6.5     #initial height of tank, m
Qmax = 208.0        #maximum demand, LPS
Qd = 0.55*Qmax       #total demand of system, as percentage of max demand LPS
Qp1 = 112.5         #initial flow through 1 pump
Qp2 = 184.12        #initial total flow through 2 pumps

def tank_vol(height, diameter):
    volume = height * np.pi * (diameter**2/4)
    return volume * 1000.0 #convert from m^3 to liters

def pump_on_off(pump_one, pump_two, tank_h):
    if tank_h > 6.3:
        pump_one = 0
    elif tank_h < 4:
        pump_one = 1
    else:
        pump_one += 0
    if tank_h > 4.5:
        pump_two = 0
    elif tank_h < 1:
        pump_two = 1
    else:
        pump_two += 0
    return pump_one, pump_two    

def pump_flow(pump1, pump2, tank_h, demand, max_demand):
    if pump1 == 0 and pump2 == 0:
        Qpump = 0
    elif pump1 == 1 and pump2 == 0:
        Qpump = (113.6 + 8.4 * (demand/max_demand)) - 1.4 * tank_h
    else:
        Qpump = (178.4 + 20.9 * (demand/max_demand)) - 2.1 * tank_h
    return Qpump

def time_calc(volume, demand): 
    t = volume / demand / 3600.0 
    return t

def slope_calc(height, time):
    s = height / time
    return s
    
def tank_height(p1_init, p2_init, height, t_step, demand, max_demand):
    pump_1, pump_2 = pump_on_off(p1_init, p2_init,height)
    time_arr = [0.0]
    height_arr = [height]
    slope = slope_calc(height, time_calc(tank_vol(initial_h, tank_dia), demand))    
    t = 0
    while height > 0:
        pf = pump_flow(pump_1, pump_2, height, demand, max_demand)
        qt = demand - pf
        slope = slope_calc(height, time_calc(tank_vol(height, tank_dia), qt)) 
        height = height - slope * t_step
        t = t + t_step
        time_arr.append(t)
        height_arr.append(height)
        pump_1, pump_2 = pump_on_off(pump_1, pump_2,height)
    return time_arr, height_arr


md = tank_height(0,1,6.5, 1.0, Qd, Qmax)

x = md[0]
y = md[1]

plt.step(x, y, where = 'mid')
plt.plot(x, y, '--o')

plt.show()


    





