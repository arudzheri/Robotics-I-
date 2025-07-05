#!/usr/bin/env python3

"""
Created on 26 Jan 2022

@author: ucacsjj
"""

# This script is needed for Q2i-l

from airport.scenarios import *
from airport.airport_environment import AirportBatteryChargingEnvironment
from airport.airport_environment import PlannerType
from airport.airport_map import MapCellType
from airport.actions import ActionType
from airport.charging_policy import ChargingPolicy
from airport.charging_policy_drawer import ChargingPolicyDrawer

if __name__ == '__main__':
    # Get the map
    airport_map = full_scenario()
    
    charging_policy = ChargingPolicy(airport_map, set_random=False)
    
    # Create the environment
    airport_environment = AirportBatteryChargingEnvironment(airport_map, planner_type=PlannerType.A_STAR)

    # Q2j, k:
    # Implement your algorithm here to use the airport_environment
    # to work out the optimal. Modify the heuristic of the planner and run again.

    for x in range(60):
        for y in range(40):
            type = airport_map.cell(x, y).cell_type()
            if type is MapCellType.SECRET_DOOR or type is MapCellType.CUSTOMS_AREA or type is MapCellType.CHARGING_STATION or type is MapCellType.OPEN_SPACE or type is MapCellType.RUBBISH_BIN:
                best_action = 0
                best_equation = -float('inf')
                for i in range(4):
                    action = (ActionType.TELEPORT_ROBOT_TO_NEW_POSITION, (x, y))
                    observation, reward, done, info = airport_environment.step(action)
                    charging_coords = airport_map.charging_station(i).coords()
                    charging_station = airport_environment.getBandit(charging_coords)
                    mean = charging_station.mean()
                    action = (ActionType.DRIVE_ROBOT_TO_NEW_POSITION, charging_coords)
                    observation, reward, done, info = airport_environment.step(action)
                    path_cost = info.path_travel_cost
                    equation = mean - path_cost
                    if equation > best_equation:
                        best_action = i
                        best_equation = equation
                charging_policy.set_action(x, y, best_action)

    
    # Plot the resulting policy
    charging_policy_drawer = ChargingPolicyDrawer(charging_policy, 200)
    charging_policy_drawer.update()
    #charging_policy_drawer.wait_for_key_press()
    
    try:
        input("Press enter in the command window to continue.....")
    except SyntaxError:
        pass
   
