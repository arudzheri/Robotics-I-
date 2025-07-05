#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

from bandits.bandit import Bandit
from bandits.bandit import BanditEnvironment
from bandits.upper_confidence_bound_agent import UpperConfidenceBoundAgent
from bandits.performance_measures import compute_percentage_of_optimal_actions_selected
from bandits.performance_measures import cumulative_regret

if __name__ == '__main__':
    # Create bandit
    environment = BanditEnvironment(4)

    # Add some bandits
    environment.set_bandit(0, Bandit(4, 1))
    environment.set_bandit(1, Bandit(4.1, 1))
    environment.set_bandit(2, Bandit(3.9, 1))
    environment.set_bandit(3, Bandit(4.2, 1))

    number_of_steps = 5000

    cs = [0.1, 0.2, 0.5, 1, 2, 4]
    percentage_correct_actions = []
    regret = []

    for c in cs:

        agent = UpperConfidenceBoundAgent(environment, c)

        # Step-by-step store of rewards
        reward_history = np.zeros(number_of_steps)
        action_history = np.zeros(number_of_steps)

        # Step through the agent and let it do its business
        for p in range(0, number_of_steps):
            action_history[p], reward_history[p] = agent.step()

        print(f'Mean reward={np.mean(reward_history)}')

        # Plot percentage correct action curves
        percentage_correct_actions.append(compute_percentage_of_optimal_actions_selected(environment, action_history))

        # Plot the regret curves
        regret.append(cumulative_regret(environment, reward_history))

    plt.plot(percentage_correct_actions[0], color='red', label='c = 0.1')
    plt.plot(percentage_correct_actions[1], color='green', label='c = 0.2')
    plt.plot(percentage_correct_actions[2], color='blue', label='c = 0.5')
    plt.plot(percentage_correct_actions[3], color='yellow', label='c = 1')
    plt.plot(percentage_correct_actions[4], color='orange', label='c = 2')
    plt.plot(percentage_correct_actions[5], color='purple', label='c = 4')
    plt.legend()
    plt.xlabel('Sample number')
    plt.ylabel('Percentage optimal action')

    plt.show()

    plt.plot(regret[0], color='red', label='c = 0.1')
    plt.plot(regret[1], color='green', label='c = 0.2')
    plt.plot(regret[2], color='blue', label='c = 0.5')
    plt.plot(regret[3], color='yellow', label='c = 1')
    plt.plot(regret[4], color='orange', label='c = 2')
    plt.plot(regret[5], color='purple', label='c = 4')
    plt.legend()
    plt.xlabel('Sample number')
    plt.ylabel('Cumulative regret')

    plt.show()
