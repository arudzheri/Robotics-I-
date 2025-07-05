"""
Created on 2 Jan 2022

@author: ucacsjj
"""

import math

from .dijkstra_planner import DijkstraPlanner


# This class implements the A* search algorithm
class AStarPlanner(DijkstraPlanner):
    
    def __init__(self, occupancyGrid):
        DijkstraPlanner.__init__(self, occupancyGrid)

    # Q2h:
    # Complete implementation of A*.

    def push_cell_onto_queue(self, cell):
        if cell.parent is None:
            dist = 0
        else:
            dist = cell.parent.dist
        dist += self.compute_lstage_additive_cost(cell.parent, cell)
        cell.dist = dist
        dist += self.compute_lstage_additive_cost(cell, self.goal)

        self.priorityQueue.put((dist, cell))

    def resolve_duplicate(self, cell, parent_cell):
        dist = self.compute_lstage_additive_cost(parent_cell, cell)
        euclid = self.compute_lstage_additive_cost(cell, self.goal)

        if parent_cell.dist + dist < cell.dist:
            cell.set_parent(parent_cell)
            cell.dist = parent_cell.dist + dist
            arr = []

            # Readd everything in the queue with the new dist to the changed cell
            while self.priorityQueue.qsize() != 0:
                current = self.priorityQueue.get()
                arr.append(current)
            for tup in arr:
                if tup[1] != cell:
                    self.priorityQueue.put(tup)
                else:
                    self.priorityQueue.put((cell.dist + euclid, tup[1]))
