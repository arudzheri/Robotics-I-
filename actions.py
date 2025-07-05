"""
Created on 25 Jan 2022

@author: ucacsjj
"""

from enum import Enum


class ActionType(Enum):
    TELEPORT_ROBOT_TO_NEW_POSITION = 0
    DRIVE_ROBOT_TO_NEW_POSITION = 1
    RECHARGE_ROBOT = 2
