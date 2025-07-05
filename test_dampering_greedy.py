#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

from bandits.bandit import Bandit
from bandits.bandit import BanditEnvironment
from bandits.damped_epsilon_greedy_agent import DampedEpsilonGreedyAgent
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

    # Q5b:
    # Change values to see what happens
    epsilons = [0.01, 0.05, 0.5, 1]
    percentage_correct_actions = []
    regret = []

    for epsilon in epsilons:

        agent = DampedEpsilonGreedyAgent(environment, epsilon)

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

    plt.plot(percentage_correct_actions[0], color='red', label='e = 0.01')
    plt.plot(percentage_correct_actions[1], color='green', label='e = 0.05')
    plt.plot(percentage_correct_actions[2], color='blue', label='e = 0.5')
    plt.plot(percentage_correct_actions[3], color='yellow', label='e = 1')
    plt.legend()
    plt.xlabel('Sample number')
    plt.ylabel('Percentage optimal action')

    plt.show()

    plt.plot(regret[0], color='red', label='e = 0.01')
    plt.plot(regret[1], color='green', label='e = 0.05')
    plt.plot(regret[2], color='blue', label='e = 0.5')
    plt.plot(regret[3], color='yellow', label='e = 1')
    plt.legend()
    plt.xlabel('Sample number')
    plt.ylabel('Cumulative regret')

    plt.show()
