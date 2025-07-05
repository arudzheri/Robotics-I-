#!/usr/bin/env python3

"""
Created on 26 Jan 2022

@author: ucacsjj
"""

from airport.scenarios import test_traversability_costs_scenario
from airport.airport_map_drawer import AirportMapDrawer
from airport.airport_environment import AirportBatteryChargingEnvironment
from airport.actions import ActionType

if __name__ == '__main__':
    
    # Create the airport for testing
    airport_map = test_traversability_costs_scenario()
    airport_map_drawer = AirportMapDrawer(airport_map, 800)
    airport_map_drawer.update()

        
    # Now create the environment
    airport_environment = AirportBatteryChargingEnvironment(airport_map)
    airport_environment.enable_verbose_graphics(True)
    
    action = (ActionType.TELEPORT_ROBOT_TO_NEW_POSITION, (7, 0))
    airport_environment.step(action)
    
    
    # Now plan a path to the 
    action = (ActionType.DRIVE_ROBOT_TO_NEW_POSITION, (7, 5))
    airport_environment.step(action)
    
    try:
        input("Press enter to continue")
    except SyntaxError:
        pass

    
    action = (ActionType.DRIVE_ROBOT_TO_NEW_POSITION, (7, 14))
    airport_environment.step(action)
        
    try:
        input("Press enter to continue")
    except SyntaxError:
        pass
    
    
