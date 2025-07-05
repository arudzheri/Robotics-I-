import time
import math
from collections import deque

from .occupancy_grid import OccupancyGrid
from .search_grid import SearchGrid
from .search_grid import SearchGridCellLabel
from .planned_path import PlannedPath

from .search_grid_drawer import SearchGridDrawer

# This class implements the basic components of the forward search
# planning algorithm in LaValle's book and the lecture slides. The
# same general framework can be used to implement a wide array of
# algorithms, including depth first search, breadth first search,
# greedy (shortest distance first) search, Dijkstra and A*. The code
# here is written to be easy to understand and is not optimised in any
# way.

# The code includes a number of hooks which do not appear in LaValle's
# description, but are useful when implementing some techniques. In
# addition, the code can optionally use a graphics library to draw the
# grid cells.

# The planner itself takes an occupancy map as an input. This
# specifies the structure of the environment - basically how big is
# it, which cells are blocked and which cells are open. The planner
# internally constructs a SearchGrid. This contains the nodes and
# edges from the planner and the labels associated with them.

class PlannerBase(object):

    # Construct a new planner object and set defaults.
    def __init__(self, environment_map):
        self._environment_map = environment_map
        self.search_grid=None

        # All these variables are used for controlling the graphics output
        self.pause_time_in_seconds = 0.05
        self.path_pause_time_in_seconds = 0.05
        self._show_graphics=True
        self._show_graphics_each_iteration=False
        self.goal_reached=None
        self.grid_drawer=None
        self.maximum_grid_drawer_window_height_in_pixels = 800
        self.draw_parent_arrows=True

    # This method pushes a cell onto the queue Q. Its implementation
    # depends upon the type of search algorithm used. If necessary,
    # (self) could also do things like update path costs as well.
    # This used in lines 2 and 11 of the pseudocode    
    def push_cell_onto_queue(self, cell):
        raise NotImplementedError()

    # This method returns a boolean - true if the queue is empty,
    # false if it still has some cells on it. Its implementation
    # depends upon the the type of search algorithm used.
    # This is used in line 3 of the pseudocode    
    def is_queue_empty(self):
        raise NotImplementedError()

    # Handle the case that a cell has been visited already. This is
    # used by some algorithms to rewrite paths to identify the
    # shortest path.
    # This corresponds to line 13 of the pseudocode    
    def resolve_duplicate(self, cell, parent_cell):
        raise NotImplementedError()

    # This method finds the first cell (at the head of the queue),
    # removes it from the queue, and returns it. Its implementation
    # depends upon the the type of search algorithm used.
    # This corresponds to line 4 of the pseudocode    
    def pop_cell_from_queue(self):
        raise NotImplementedError()

    # This method determines if the goal has been reached.
    # This corresponds to line 5 of the pseudocode    
    def has_goal_been_reached(self, cell):
        return cell == self.goal

    # Compute the additive cost of performing a step from the parent to the
    # current cell. This calculation is carried out the same way no matter
    # what heuristics, etc. are used
    def compute_lstage_additive_cost(self, parentCell, cell):
        
        # If the parent is empty, this is the start of the path and the
        # cost is 0.
        if (parentCell is None):
            return 0
        
        # Use the environment map to compute what the transition cost is
        cell_coords = cell.coords()
        parent_cell_coords = parentCell.coords()
        
        return self._environment_map.compute_transition_cost(parent_cell_coords, cell_coords)

    # This method gets the list of cells which potentially could be
    # visited next. Each candidate position has to be tested
    # separately.
    # This corresponds to line 7 of the pseudocode    
    def next_cells_to_be_visited(self, cell):

        # This stores the set of valid actions / cells
        cells = list()

        #Q3b
        # Modify so that the cells are visited in a different sequence.
        # Investigate the impact of changing the search order on the computed path

        # Go through all the neighbours and add the cells if they
        # don't fall outside the grid and they aren't the cell we
        # started with. The order has been manually written down to
        # create a spiral.

        # The swapped order video transposed the last four transitions first
        self.push_back_candidate_cell_if_valid(cell, cells, 0, -1)
        self.push_back_candidate_cell_if_valid(cell, cells, 1, -1)
        self.push_back_candidate_cell_if_valid(cell, cells, 1, 0)
        self.push_back_candidate_cell_if_valid(cell, cells, 1, 1)
        self.push_back_candidate_cell_if_valid(cell, cells, 0, 1)
        self.push_back_candidate_cell_if_valid(cell, cells, -1, 1)
        self.push_back_candidate_cell_if_valid(cell, cells, -1, 0)
        self.push_back_candidate_cell_if_valid(cell, cells, -1, -1)

        return cells

    # This helper method checks if the robot, at cell.coords, can move
    # to cell.coords+(offsetX, offsetY). Reasons why it can't do (self)
    # include falling off the edge of the map or running into an
    # obstacle.
    def push_back_candidate_cell_if_valid(self, cell, cells, offsetX, offsetY):
        cellCoords = cell.coords()
        newX = cellCoords[0] + offsetX
        newY = cellCoords[1] + offsetY
        if ((newX >=0) & (newX < self._environment_map.width()) \
            & (newY >=0) & (newY < self._environment_map.height())):
            newCoords = (newX, newY)
            newCell = self.search_grid.cell_from_coords(newCoords)
            if newCell.is_obstructed is False:
                cells.append(newCell)

    # This method determines whether a cell has been visited already.
    # This corresponds to line 9 of the pseudocode    
    def has_cell_been_visited_already(self, cell):
        return cell.label() != SearchGridCellLabel.UNVISITED

    # Mark that the cell has been visited. Also note the parent, which
    # is used to extract the path later on.
    # This corresponds to line 10 of the pseudocode    
    def mark_cell_as_visited_and_record_parent(self, cell, parentCell):
        cell.set_label(SearchGridCellLabel.ALIVE)
        cell.set_parent(parentCell)

    # Mark that a cell is dead. A dead cell is one in which all of its
    # immediate neighbours have been visited.
    # This corresponds to line 14 of the pseudocode    
    def mark_cell_as_dead(self, cell):
        cell.set_label(SearchGridCellLabel.DEAD)
        
    # The main search routine. Given the input startCoords (x,y) and
    # goalCoords (x,y), compute a plan. Note that the coordinates
    # index from 0 and refer to the cell number.
    def plan(self, start_coords, goal_coords):

        # Empty the queue. This is needed to make sure everything is reset
        while (self.is_queue_empty() == False):
            self.pop_cell_from_queue()
        
        # Create the search grid from the occupancy grid and seed
        # unvisited and occupied cells.
        if (self.search_grid is None):
            self.search_grid = SearchGrid.from_environment_map(self._environment_map)
        else:
            self.search_grid.set_from_environment_map(self._environment_map)

        # Get the start cell object and label it as such. Also set its
        # path cost to 0.
        self.start = self.search_grid.cell_from_coords(start_coords)
        self.start.is_start=True
        self.start.path_cost = 0

        # Get the goal cell object and label it.
        self.goal = self.search_grid.cell_from_coords(goal_coords)
        self.goal.is_goal=True

        # If required, set up the grid drawer and show the initial state
        if (self._show_graphics == True):
            if (self.grid_drawer is None):
                self.grid_drawer = SearchGridDrawer(self.search_grid, self.maximum_grid_drawer_window_height_in_pixels)
            else:
                self.grid_drawer.reset()
            self.draw_current_state()
            #self.grid_drawer.wait_for_key_press()

        # Insert the start on the queue to start the process going.
        self.mark_cell_as_visited_and_record_parent(self.start, None)
        self.push_cell_onto_queue(self.start)

        # Reset the count
        self.number_of_cells_visited = 0

        # Indicates if we reached the goal or not
        self.goal_reached=False
        
        # Iterate until we have run out of live cells to try or we reached the goal
        # This corresponds to lines 3-15 of the pseudocode
        while (self.is_queue_empty() == False):
            cell = self.pop_cell_from_queue()
            if (self.has_goal_been_reached(cell) == True):
                self.goal_reached=True
                break
            cells = self.next_cells_to_be_visited(cell)
            for nextCell in cells:
                if (self.has_cell_been_visited_already(nextCell) == False):
                    self.mark_cell_as_visited_and_record_parent(nextCell, cell)
                    self.push_cell_onto_queue(nextCell)
                    self.number_of_cells_visited = self.number_of_cells_visited + 1
                else:
                    self.resolve_duplicate(nextCell, cell)

            # Now that we've checked all the actions for (self) cell,
            # mark it as dead
            self.mark_cell_as_dead(cell)

            # Draw the update if required
            if (self._show_graphics_each_iteration == True):
                self.draw_current_state()

        # Draw the final results if required
        self.draw_current_state()

        if (self.goal_reached == True):
            print (f'Reached the goal after visiting {self.number_of_cells_visited} cells')
        else:
            print (f'Could not reach the goal after visiting {self.number_of_cells_visited} cells')
            
        return self.goal_reached


    # This method extracts a path from the pathEndCell to the start
    # cell. The path is a list actually sorted in the order:
    # cell(x_I), cell(x_1), ... , cell(x_K), cell(x_G). You can use
    # (self) method to try to find the path from any end cell. However,
    # depending upon the planner used, the results might not be
    # valid. In (self) case, the path will probably not terminate at the
    # start cell.
    def extract_path(self, path_end_cell):

        # Construct the path object and mark if the goal was reached
        path = PlannedPath()
        path.goal_reached = self.goal_reached
        
        # Initial condition - the goal cell
        path.waypoints.append(path_end_cell)
               
        # Start at the goal and find the parent
        cell = path_end_cell.parent

        while (cell is not None):
            
            # Add to the list
            path.waypoints.appendleft(cell)
                       
            if (cell.is_start is False) and (cell.is_goal is False):
                cell.is_on_path=True

            if (self._show_graphics == True):
                self.grid_drawer.update()
                time.sleep(self.path_pause_time_in_seconds)

            cell = cell.parent
            
        path.number_of_cells_visited = self.number_of_cells_visited
            
        # If we didn't reach the goal, the cost is infinite
        if self.goal_reached is False:
            path.path_travel_cost = float('inf')
            return path
            
        # Now go forwards through the path and construct the cost. We could do it
        # going backwards at path assembly time, but this is easier!
        path_cost = 0
        
        for cell in path.waypoints:
            if cell.parent is not None:
                path_cost = path_cost + \
                    self._environment_map.compute_transition_cost(cell.parent.coords(), cell.coords())

        path.path_travel_cost = path_cost

        # Return the path
        return path

    # Extract the path between the start and goal.
    def extract_path_to_goal(self):
        path = self.extract_path(self.goal)
        return path
    
    # Draw the output and sleep for the pause time.
    def draw_current_state(self):
        if (self._show_graphics == True):
            self.grid_drawer.update()
            time.sleep(self.pause_time_in_seconds)

    # Set the pause time
    def set_pause_time(self, pauseTimeInSeconds):
        self.pause_time_in_seconds = pauseTimeInSeconds
        
    # Set the pause time for showing the path
    def set_path_pause_time(self, pathPauseTimeInSeconds):
        self.path_pause_time_in_seconds = pathPauseTimeInSeconds
        
    def show_parent_arrows(self, drawParentArrows):    
        self.draw_parent_arrows = drawParentArrows
    
    # Specify if we show graphics on each iteration
    def update_graphics_each_iteration(self, updateGraphicsEachIteration):
        self._show_graphics_each_iteration = updateGraphicsEachIteration
        
    def show_graphics(self, show_graphics):
        self._show_graphics = show_graphics
        
