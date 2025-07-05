"""
Created on 26 Jan 2022

@author: ucacsjj
"""

# This array summarises the cell charging policy - for each cell 
# it specifies the charging station number the robot should go to

from random import randint

from grid_search.grid import Grid


class ChargingPolicy(Grid):
    """
    classdocs
    """

    def __init__(self, airport_map, set_random=False):
        Grid.__init__(self, "Charging Policy", airport_map.width(), airport_map.height())

        # Set the initial policy - either to all -1 (not set) or a random number
        # between -1 and the number of charging stations        
        if set_random is False:
            self._policy = [[-1 for y in range(self._height)] \
                            for x in range(self._width)]
        else:
            num_charging_stations = len(airport_map.all_charging_stations())
            self._policy = [[randint(-1, num_charging_stations) for y in range(self._height)] \
                            for x in range(self._width)]

    def set_action(self, x, y, action):
        self._policy[x][y] = action

    def action(self, x, y):
        return self._policy[x][y]
