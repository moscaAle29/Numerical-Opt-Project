#!/usr/bin/python3
import numpy as np


class Agent():
    def __init__(self):
        print("Agent::__init__")
        pass

    def get_action(self, obs):
        print("Agent::get_action")
        act = []
        # 
        # SATISFY ORDERS:
        for i, order in enumerate(obs['order']):
            # get first position of in whiche there is a ordered block
            pos = np.transpose(
                np.where(obs['actual_warehouse'].disposition == order)
            )[0]
            row, col = pos[0], pos[1]
            for ii in range(0, row):
                if obs['actual_warehouse'].disposition[ii, col] != 0:
                    # move to the last column the parcel
                    act.append(
                        {
                            'type': 'P',
                            'col1': 0,
                            'col2': obs['actual_warehouse'].n_cols - 1,
                        }
                    )
            
            act.append(
                {'type': 'O', 'col': col, 'n_order': i}
            )
            
        # LOCATE NEW PARCELS
        for i, parcel in enumerate(obs['new_parcel']):
            for col in range(obs['actual_warehouse'].n_cols):
                if obs['actual_warehouse'].disposition[0, col]==0:
                    act.append(
                        {'type': 'N', 'n_parcel': i, 'col': col}
                    )
                    obs['actual_warehouse']._locate(
                        parcel,
                        col
                    )
                    break
                
        return act
    

    def learn(self, iterations = 10):
        pass
