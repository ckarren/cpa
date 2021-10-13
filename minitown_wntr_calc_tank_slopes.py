import wntr
import wntr.network.controls as controls
import numpy as np
#use dictionaries...
demands = [1.0, 0.75,  0.5, 0.25, 0.0]
def get_tank_slopes(inp_file):
    slope_array_p1 = []
    slope_array_p2 = []
    for i in [1,2]:
        num_pumps = i
        for d in demands:
            net = wntr.network.WaterNetworkModel(inp_file)
            pump1 = net.get_link('PUMP1')
            pump2 = net.get_link('PUMP2')
            tank = net.get_node('TANK')
            for junction_name, junction in net.junctions():
                junction.demand_timeseries_list[0].base_value = junction.demand_timeseries_list[0].base_value * d
            if num_pumps == 0:
                pump1.initial_status = 'CLOSED'
                pump2.initial_status = 'CLOSED'
                tank.init_level = 6.5
            elif num_pumps == 1:
                pump1.initial_status = 'OPEN'
                pump2.initial_status = 'CLOSED'
                if d <= 0.5:
                    #TODO figure out maximum demand that can be met by the tank without pumps
                    tank.init_level = 0.0
                else:
                    tank.init_level = 6.5
            else:
                pump1.initial_status = 'OPEN'
                pump2.initial_status = 'OPEN'
                if d <= 0.75:
                #TODO figure out maximum demand that can be met by the tank without pumps
                    tank.init_level = 0.0
                else:
                    tank.init_level = 6.5                                                
            sim = wntr.sim.EpanetSimulator(net)
            results = sim.run_sim()
            tank_height = results.node['pressure'].loc[:,'TANK']
            flow_p1 = results.link['flowrate'].loc[:, 'PUMP1']*1000     #get flowrate through PUMP1 for all times, convert from m^3/s -> LPS
            flow_p2 = results.link['flowrate'].loc[:,'PUMP2']*1000      #get flowrate through PUMP1 for all times, convert from m^3/s -> LPS
            flow_ptot = flow_p1 + flow_p2
            if tank.init_level == 6.5:
                x = [i for i in tank_height.values if i > 0.01]
            elif tank.init_level == 0.0:
                x = [i for i in tank_height.values if i < 6.49]
            y =  flow_ptot.values[0:len(x)]
            linear_model=np.polyfit(x,y,1)
            if i == 1:
                slope_array_p1.append(linear_model)
            else:
                slope_array_p2.append(linear_model)
            net.reset_initial_values()
    return slope_array_p1, slope_array_p2
slope_list_p1, slope_list_p2 = get_tank_slopes('minitown_map_maxdemand.inp')
#slope_list_p2 = get_tank_slopes('minitown_map_maxdemand.inp')[1]
def get_slope(sl):
    intercepts = []
    for i in range(len(sl)):
        intercepts.append(sl[i][1])
    y2 = intercepts
    x2 = demands
    linear_intercepts = np.polyfit(x2,y2, 1)
    return linear_intercepts

print(get_slope(slope_list_p2))


