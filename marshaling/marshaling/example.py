from agent.QLearningAgent import QLearningAgent
from env.ModifiedWarehouse import ModifiedWarehouse
import numpy as np


n_rows = 3
n_cols = 3
time_limit = 10
n_parcel_types = 3

qTable = np.zeros(((n_parcel_types+1)**(n_cols*n_rows), n_cols*(n_cols - 1)), dtype=int)
alpha = 0.5
gamma = 0.5
epsilon = 0.1

agent = QLearningAgent(qTable, alpha, gamma, epsilon)
env = ModifiedWarehouse(n_parcel_types, n_rows, n_cols)


for i in range(0, 1000):
    agent.learn(env)

print(qTable)