from agent.QLearningAgent import QLearningAgent
from env.ModifiedWarehouse import ModifiedWarehouse
import numpy as np


n_rows = 3
n_cols = 3
n_parcel_types = 3

qTable = np.zeros(((n_parcel_types+1)**(n_cols*n_rows), n_cols*(n_cols - 1)), dtype=int)
alpha = 0.5
gamma = 0.5
epsilon = 1

agent = QLearningAgent(qTable, alpha, gamma, epsilon)
env = ModifiedWarehouse(n_parcel_types, n_rows, n_cols)


for i in range(0, 1000):
    agent.learn(env)
    agent.epsilon = agent.epsilon - 0.0005

time_limit = 10
tot_cost = 0
obs = env.reset()
for t in range(time_limit):
    action = agent.get_action(obs)
    obs, cost, info = env.step(action)
    tot_cost += cost
    print(env.disposition.disposition)
    env.plot()
    print("---")

print(tot_cost)

