import numpy as np

from bandits.bandit import Bandit
from bandits.bandit import BanditEnvironment
from bandits.try_them_all_agent import TryThemAllAgent

if __name__ == '__main__':
    # Create bandit
    environment = BanditEnvironment(4)

    # Add some bandits
    environment.set_bandit(0, Bandit(4, 1))
    environment.set_bandit(1, Bandit(4.1, 1))
    environment.set_bandit(2, Bandit(3.9, 1))
    environment.set_bandit(3, Bandit(4.2, 1))

    number_of_steps = 10000

    number_of_tries = 100

    agent = TryThemAllAgent(environment, number_of_tries)

    # Step-by-step store of rewards
    reward_history = np.zeros(number_of_steps)
    action_history = np.zeros(number_of_steps)

    # Step through the agent and let it do its business
    for p in range(0, number_of_steps):
        action_history[p], reward_history[p] = agent.step()

    print(f'Mean reward={np.mean(reward_history)}')
