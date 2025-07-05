"""
Created on 26 Jan 2022

@author: ucacsjj
"""

from grid_search.grid_drawer import GridDrawer


class ChargingPolicyDrawer(GridDrawer):
    """
    classdocs
    """

    def __init__(self, charging_policy, maximum_grid_drawer_window_height_in_pixels, top_left_in_pixels=None):

        GridDrawer.__init__(self, charging_policy, maximum_grid_drawer_window_height_in_pixels, top_left_in_pixels)
  
        self._charging_action_colours = {
            0 : 'red',
            1 : 'green',
            2 : 'blue',
            3 : 'magenta'}
        
        self._default_colour = 'gray'
  
    def update(self):

        ### Figure out the width and height
        width = self._grid.width()
        height = self._grid.height()

        for x in range(width):
            for y in range(height):
                
                # First update the grid cell
                action = self._grid.action(x, y)
                
                colour = self._charging_action_colours.get(action, self._default_colour)
                
                self._rectangles[y][x].setFill(colour)
                
        # Flush the drawing right at the very end for speed
        self._win.flush()      
