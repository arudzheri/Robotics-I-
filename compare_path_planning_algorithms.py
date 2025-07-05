#!/usr/bin/env python3

"""
Created on 27 Jan 2022

@author: ucacsjj
"""

from airport.scenarios import *
from airport.airport_environment import PlannerType
from airport.airport_environment import AirportBatteryChargingEnvironment
from airport.actions import ActionType

if __name__ == '__main__':
    
    # Create the scenario
    airport_map = full_scenario()
    
    # Create the gym environment
    airport_environment = AirportBatteryChargingEnvironment(airport_map, PlannerType.BREADTH_FIRST)
    airport_environment1 = AirportBatteryChargingEnvironment(airport_map, PlannerType.DEPTH_FIRST)
    airport_environment2 = AirportBatteryChargingEnvironment(airport_map, PlannerType.DIJKSTRA)
    airport_environment3 = AirportBatteryChargingEnvironment(airport_map, PlannerType.A_STAR)
    
    # Set the graphics debugging to full
    airport_environment.enable_verbose_graphics(True)
    airport_environment1.enable_verbose_graphics(True)
    airport_environment2.enable_verbose_graphics(True)
    airport_environment3.enable_verbose_graphics(True)
    
    # First specify the start location of the robot
    action = (ActionType.TELEPORT_ROBOT_TO_NEW_POSITION, (0, 0))
    observation, reward, done, info = airport_environment.step(action)
    observation1, reward1, done1, info1 = airport_environment1.step(action)
    observation2, reward2, done2, info2 = airport_environment2.step(action)
    observation3, reward3, done3, info3 = airport_environment3.step(action)
    
    if reward is -float('inf'):
        print('Unable to teleport to (1, 1)')
        
    # Get all the rubbish bins and toilets; these are places which need cleaning
    all_rubbish_bins = airport_map.all_rubbish_bins()
        
    # Q2b
    # Modify this code to collect the data needed to assess the different algorithms

    total_cost = 0
    total_cells = 0
    
    # Now go through them and plan a path sequentially
    for rubbish_bin in all_rubbish_bins:
        action = (ActionType.DRIVE_ROBOT_TO_NEW_POSITION, rubbish_bin.coords())
        observation, reward, done, info = airport_environment3.step(action)
        total_cells += info.number_of_cells_visited
        total_cost += info.path_travel_cost

    print("Total cells: " + str(total_cells))
    print("Total cost: " + str(total_cost))
    
    try:
        input("Press enter in the command window to continue.....")
    except SyntaxError:
        pass  
    
