'''
Created on 29 Jan 2022

@author: ucacsjj
'''

from .dynamic_programming_base import DynamicProgrammingBase
from airport.driving_actions import DrivingActionType

# This class ipmlements the value iteration algorithm

class ValueIterator(DynamicProgrammingBase):

    def __init__(self, environment):
        DynamicProgrammingBase.__init__(self, environment)
        
        # The maximum number of times the value iteration
        # algorithm is carried out is carried out.
        self._max_optimal_value_function_iterations = 2000
        self.iterations = 0
   
    # Method to change the maximum number of iterations
    def set_max_optimal_value_function_iterations(self, max_optimal_value_function_iterations):
        self._max_optimal_value_function_iterations = max_optimal_value_function_iterations

    #    
    def solve_policy(self):

        # Initialize the drawers
        if self._policy_drawer is not None:
            self._policy_drawer.update()
            
        if self._value_drawer is not None:
            self._value_drawer.update()
        
        self._compute_optimal_value_function()
 
        self._extract_policy()
        
        # Draw one last time to clear any transients which might
        # draw changes
        if self._policy_drawer is not None:
            self._policy_drawer.update()
            
        if self._value_drawer is not None:
            self._value_drawer.update()
        
        return self._v, self._pi

    # Q3h: Finish implementation of the value iterator
    
    def _compute_optimal_value_function(self):
        environment = self._environment
        map = environment.map()

        iteration = 0

        while True:
            delta = 0

            for x in range(map.width()):
                for y in range(map.height()):
                    if map.cell(x, y).is_obstruction() or map.cell(x, y).is_terminal():
                        continue

                    cell = (x, y)
                    old_v = self._v.value(x, y)
                    best_v = -float('inf')

                    for action in range(8):
                        s_prime, r, p = environment.next_state_and_reward_distribution(cell, DrivingActionType(action))

                        new_v = 0
                        for t in range(len(p)):
                            sc = s_prime[t].coords()
                            new_v = new_v + p[t] * (r[t] + self._gamma * self._v.value(sc[0], sc[1]))

                        if new_v > best_v:
                            best_v = new_v
                        # Set the new value in the value function
                    self._v.set_value(x, y, best_v)

                    # Update the maximum deviation
                    delta = max(delta, abs(old_v - best_v))

            iteration += 1

            print(f'Finished policy evaluation iteration {iteration}')

            if (delta < self._theta) or (iteration >= self._max_optimal_value_function_iterations):
                self.iterations = iteration
                break

    def _extract_policy(self):
        environment = self._environment
        map = environment.map()

        for x in range(map.width()):
            for y in range(map.height()):
                if map.cell(x, y).is_obstruction() or map.cell(x, y).is_terminal():
                    continue

                cell = (x, y)

                best_v = -float('inf')
                best_action = 0

                for action in range(8):
                    s_prime, r, p = environment.next_state_and_reward_distribution(cell, DrivingActionType(action))

                    new_v = 0
                    for t in range(len(p)):
                        sc = s_prime[t].coords()
                        new_v = new_v + p[t] * (r[t] + self._gamma * self._v.value(sc[0], sc[1]))

                    if new_v > best_v:
                        best_v = new_v
                        best_action = action

                self._pi.set_action(x, y, best_action)
