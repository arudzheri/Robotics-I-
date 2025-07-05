

import numpy as np
import pandas as pd
import gym
import seaborn as sns
import matplotlib.pyplot as plt

from bandits.bandit import Bandit
from bandits.bandit import BanditEnvironment


def run_bandits(environment, number_of_steps, d):
    for b in range(0, environment.number_of_bandits()):
        rewards = np.zeros(number_of_steps)
        for s in range(0, number_of_steps):
            obs, reward, done, info = environment.step(b)
            rewards[s] = reward
            d['charging_station'].append(b+1)
            d['reward'].append(reward)

        print(f'bandit={b}, mean={np.mean(rewards)}, sigma={np.std(rewards)}')


if __name__ == '__main__':

    environment = BanditEnvironment(4)

    # Add some bandits
    environment.set_bandit(0, Bandit(4, 1))
    environment.set_bandit(1, Bandit(4.1, 1))
    environment.set_bandit(2, Bandit(3.9, 1))
    environment.set_bandit(3, Bandit(4.2, 1))


    # Vary the number of steps if you like to validate your code
    d = {'charging_station': [], 'reward': []}
    run_bandits(environment, 2000, d)
    df = pd.DataFrame(d)

    #plot
    sns.violinplot(x="charging_station", y="reward", data=df)
    plt.show()


