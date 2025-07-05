"""
Created on 14 Jan 2022

@author: ucacsjj
"""

from .agent import Agent


# This agent randomly picks action
class RandomActionAgent(Agent):

    # Construct the agent. Because we do nothing here,
    # we could avoid the need for a constructor. However, I personally find
    # it cleaner to add to remind myself what the constructor looks like
    def __init__(self, environment):
        super().__init__(environment)
        
    # Q3a:
    # Choose a random action the agent will perform
    def _choose_action(self):
        return self._environment.action_space.sample()

        
