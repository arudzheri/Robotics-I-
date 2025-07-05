#!/usr/bin/env python3

"""
Created on 25 Jan 2022

@author: ucacsjj
"""

from airport.scenarios import *
from airport.airport_map_drawer import AirportMapDrawer

if __name__ == '__main__':
    airport = full_scenario()
    airport_map_drawer = AirportMapDrawer(airport, 200)
    
    airport_map_drawer.update()
    
    airport_map_drawer.wait_for_key_press()

    
