from math import sqrt
from queue import PriorityQueue

from .planner_base import PlannerBase

class GreedyShortestDistancePlanner(PlannerBase):

    # This order the cells on a priority queue, sorted in terms of distance to target: shorter is better
    
    def __init__(self, occupancyGrid):
        PlannerBase.__init__(self, occupancyGrid)
        self.priorityQueue = PriorityQueue()

    # Sort in order of distance from the target and use that
    def push_cell_onto_queue(self, cell):

        # Distance to the goal
        cellCoords = cell.coords()
        goalCoords = self.goal.coords()

        dX = cellCoords[0] - goalCoords[0]
        dY = cellCoords[1] - goalCoords[1]
        d = sqrt(dX * dX + dY * dY)
        self.priorityQueue.put((d, cell))

    # Check the queue size is zero
    def is_queue_empty(self):
        return self.priorityQueue.empty()

    # Simply pull from the front of the list
    def pop_cell_from_queue(self):
        t = self.priorityQueue.get()
        return t[1]

    def resolve_duplicate(self, cell, parent_cell):
        # Nothing to do in this case
        pass
