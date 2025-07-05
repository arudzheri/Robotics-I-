#!/usr/bin/env python3


"""
Created on 25 Jan 2022

@author: ucacsjj
"""

from airport.scenarios import mini_scenario
from airport.airport_environment import AirportBatteryChargingEnvironment
from airport.actions import ActionType

# This script illustrates how to use the airport environment

if __name__ == '__main__':
    airport_map = mini_scenario()
    airport_environment = AirportBatteryChargingEnvironment(airport_map)
    airport_environment.enable_verbose_graphics(True)
    
    # Teleport is always used to put the robot in the right place
    action = (ActionType.TELEPORT_ROBOT_TO_NEW_POSITION, (1, 1))
    airport_environment.step(action)

    # Run the path planner a couple of times
    action = (ActionType.DRIVE_ROBOT_TO_NEW_POSITION, (4, 4))
    observation, reward, done, info = airport_environment.step(action)
    
    action = (ActionType.DRIVE_ROBOT_TO_NEW_POSITION, (14, 4))
    observation, reward, done, info = airport_environment.step(action)
    
    # Now drive to a recharging station
    charging_station = airport_map.charging_station(0)
    action = (ActionType.DRIVE_ROBOT_TO_NEW_POSITION, charging_station.coords())
    observation, reward, done, info = airport_environment.step(action)

    # Ping off of the bandit where the     
    # Note the trailing comma that's needed to create a single element tuple.
    
    # In your solutions, consider whether you need to use this    
    total_reward = 0
    for i in range(1000):
        action = (ActionType.RECHARGE_ROBOT, )
        observation, reward, done, info = airport_environment.step(action)
        total_reward += reward
    print(f'Average reward from the bandit = {total_reward/1000}')
    
    try:
        input("Press enter in the command window to continue.....")
    except SyntaxError:
        pass  
    
