"""
Created on 2 Jan 2022

@author: ucacsjj
"""

from math import sqrt
from queue import PriorityQueue

from .planner_base import PlannerBase


class DijkstraPlanner(PlannerBase):

    # This implements Dijkstra. The priority queue is the path length
    # to the current position.
    
    def __init__(self, occupancyGrid):
        PlannerBase.__init__(self, occupancyGrid)
        self.priorityQueue = PriorityQueue()

    # Q2d:
    # Modify this class to finish implementing Dijkstra

    def push_cell_onto_queue(self, cell):
        if cell.parent is None:
            dist = 0
        else:
            dist = cell.parent.dist
        dist += self.compute_lstage_additive_cost(cell.parent, cell)
        cell.dist = dist

        self.priorityQueue.put((dist, cell))

    # Check the queue size is zero
    def is_queue_empty(self):
        return self.priorityQueue.empty()

    # Simply pull from the front of the list
    def pop_cell_from_queue(self):
        cell = self.priorityQueue.get()[1]
        return cell

    def resolve_duplicate(self, cell, parent_cell):
        dist = self.compute_lstage_additive_cost(parent_cell, cell)

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
                    self.priorityQueue.put((cell.dist, tup[1]))
        
