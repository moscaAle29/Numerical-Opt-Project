#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
from agent.agent import Agent
from env.warehouse import Warehouse

np.random.seed(1)

if __name__ == '__main__':
    # parameters
    n_rows = 3
    n_cols = 4
    time_limit = 3
    n_parcel_types = 3

    env = Warehouse(
        n_parcel_types=n_parcel_types,
        n_rows=n_rows,
        n_cols=n_cols
    )
    obs = env.reset()
    # env.plot()
    agent = Agent()
    tot_cost = 0
    for t in range(time_limit):
        action = agent.get_action(obs)
        obs, cost, info = env.step(action)
        tot_cost += cost
        print(env.disposition.disposition)
        env.plot()
        print("---")
    print(tot_cost)
