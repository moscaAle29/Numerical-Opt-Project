#!/usr/bin/python3
import gym
import copy
import random
import numpy as np
from env.grid import Grid
import matplotlib.pyplot as plt


class Warehouse(gym.Env):
    def __init__(self, n_parcel_types, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.disposition = Grid(n_rows=n_rows, n_cols=n_cols)
        self.n_parcel_types = n_parcel_types

    def reset(self): 
        obs = self._get_obs()
        return obs

    def _get_obs(self):
    
        non_zeroes = np.transpose(np.nonzero(self.disposition.disposition))
        n_orders = 1
        n_parcels = np.random.randint(
            low=1,
            # leave a column for moving objects
            high=min(3, self.n_cols * (self.n_rows-1) - len(non_zeroes))
        )

        self.orders = []
        if len(non_zeroes) > 0:
            for rnd_pos in random.sample(range(len(non_zeroes)), n_orders):
                self.orders.append(
                    self.disposition.disposition[non_zeroes[rnd_pos][0], non_zeroes[rnd_pos][1]]
                )
        self.new_parcels = np.random.randint(
            low=1,
            high=4,
            size=(n_parcels,)
        )

        obs = {
            'actual_warehouse': copy.deepcopy(self.disposition),
            'order': self.orders,
            'new_parcel': self.new_parcels
        }
        return obs

    def step(self, action):
        cost = len(action)
        for move in action:
            # position of the new
            if move['type'] == 'N':
                self.disposition._locate(
                    self.new_parcels[move['n_parcel']],
                    col=move['col']
                )
            elif move['type'] == 'O':
                parcel_get = self.disposition._take(move['col'])
                if parcel_get != self.orders[move['n_order']]:
                    ValueError('Shipped wrong parcel')
            else:
                self.disposition._move(
                    move['col1'],
                    move['col2']
                )
        obs = self._get_obs()
        info = {}
        return obs, cost, info

    def plot(self, file_path=None):
        fig, ax = plt.subplots()
        # remove from the print all the zero values
        data_masked = np.ma.masked_where(
            self.disposition.disposition == 0, self.disposition.disposition
        )
        ax.imshow(data_masked, interpolation = 'none',aspect='equal', vmin = 1)
        
        # Show all ticks and label them with the respective list entries
        ax.set_xticks(np.arange(self.n_cols), labels=range(self.n_cols))
        ax.set_yticks(np.arange(self.n_rows), labels=range(self.n_rows))

        # Loop over data dimensions and create text annotations.
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                ax.text(
                    j, i, self.disposition.disposition[i, j],
                    ha="center", va="center", color="w"
                )
        fig.tight_layout()
        # plot or save
        if file_path:
            plt.savefig(file_path)
            plt.close()
        else:
            plt.show()
        