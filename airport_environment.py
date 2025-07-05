"""
Created on 25 Jan 2022

@author: ucacsjj
"""

from enum import Enum

import gym

# Import the planners
from grid_search.a_star_planner import AStarPlanner
from grid_search.breadth_first_planner import BreadthFirstPlanner
from grid_search.depth_first_planner import DepthFirstPlanner
from grid_search.dijkstra_planner import DijkstraPlanner

from bandits.bandit import Bandit
from .actions import ActionType


class PlannerType(Enum):
    BREADTH_FIRST = 0
    DEPTH_FIRST = 1
    DIJKSTRA = 2
    A_STAR = 3


class AirportBatteryChargingEnvironment(gym.Env):
    """
    classdocs
    """

    def __init__(self, airport_map, planner_type = PlannerType.DEPTH_FIRST):
        """
        Constructor
        """

        # Store the map
        self._airport_map = airport_map

        # Create the planner which will be used to simulate the robot's travel
        planner_factory = {
            PlannerType.BREADTH_FIRST: BreadthFirstPlanner(self._airport_map),
            PlannerType.DEPTH_FIRST: DepthFirstPlanner(self._airport_map),
            PlannerType.DIJKSTRA: DijkstraPlanner(self._airport_map),
            PlannerType.A_STAR: AStarPlanner(self._airport_map),
        }
        self._planner = planner_factory.get(planner_type)

        # Disable the graphics by default; this can be enabled again
        self._planner.show_graphics(False)

        # Create the bandits which will be used for charging
        charging_stations = airport_map.all_charging_stations()
        self._charging_station_bandits = {}
        for b in range(len(charging_stations)):
            params = charging_stations[b].params()
            bandit = Bandit(params[0], params[1])
            self._charging_station_bandits[charging_stations[b].coords()] = bandit

        self._current_coords=None

    def getBandit(self, num):
        return self._charging_station_bandits[num]

    def reset(self):
        self._current_coords=None
        return self._current_coords

    def planner(self):
        return self._planner

    def enable_verbose_graphics(self, verbose_graphics):
        self._planner.show_graphics(verbose_graphics)

    def step(self, action):
        # If the action is to teleport the robot to a new location,
        # do so instantly at no cost. If the robot  can't be 
        # transported to the new cell, return a reward of -infinity
        # and leave the robot as-is.
        if action[0] == ActionType.TELEPORT_ROBOT_TO_NEW_POSITION:
            new_coords = action[1]
            if self._airport_map.is_obstructed(new_coords[0], new_coords[1]):
                return self._current_coords, -float("inf"), False, False
            else:
                self._current_coords = action[1]
                return self._current_coords, 0, False, True

        # If the action is to plan a path to the new goal, fire up
        # our planner and get the path. Here we only care about the path cost.
        # If the path can be reached we return the negative of the path cost
        # (because we want to maximise reward and minimize the path length).
        # If the goal can't be reached, the reward is minus infinity
        if action[0] == ActionType.DRIVE_ROBOT_TO_NEW_POSITION:
            goal_coords = action[1]
            self._planner.plan(self._current_coords, goal_coords)
            plan = self._planner.extract_path_to_goal()
            print(f'plan.path_travel_cost = {plan.path_travel_cost}')
            if plan.goal_reached is True:
                self._current_coords = goal_coords
                return self._current_coords, -plan.path_travel_cost, False, plan
            else:
                return self._current_coords, -float("inf"), False, plan

        # If the action is to recharge the robot, this action can only be carried out at
        # the charging station, otherwise the cost is infinitely negative. If the robot
        # is at a charging station, figure out which one it is, extract the bandit and
        # pull the arm.
        if action[0] == ActionType.RECHARGE_ROBOT:
            if self._current_coords in self._charging_station_bandits:
                charging_station_bandit = self._charging_station_bandits[self._current_coords]
                return self._current_coords, charging_station_bandit.pull_arm(), False, True
            else:
                return self._current_coords, -float("inf"), False, False
