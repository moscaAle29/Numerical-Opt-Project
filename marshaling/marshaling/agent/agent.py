#!/usr/bin/python3
import numpy as np
import copy

class Agent():
    def __init__(self):
        print("Agent::__init__")
        pass

    def get_action(self, obs):
        print("Agent::get_action")
        copiedObs = {
            'actual_warehouse' : copy.deepcopy(obs['actual_warehouse']),
            'order': obs['order'],
            'new_parcel': obs['new_parcel']
        }

        copiedObs['actual_warehouse'].disposition = obs['actual_warehouse'].disposition.copy()

        act = []
        # 
        # SATISFY ORDERS:
        for i, order in enumerate(copiedObs['order']):
            # get first position of in whiche there is a ordered block
            pos = np.transpose(
                np.where(copiedObs['actual_warehouse'].disposition == order)
            )[0]
            row, col = pos[0], pos[1]
            for ii in range(0, row):
                if copiedObs['actual_warehouse'].disposition[ii, col] != 0:
                    # move to the last column the parcel
                    #act.append(
                    #    {
                    #        'type': 'P',
                    #        'col1': col,
                    #        'col2': obs['actual_warehouse'].n_cols - 1,
                    #    }
                    #)

                    #move to any column that is not full
                    for c in range(0, copiedObs['actual_warehouse'].n_cols):
                        if (c != col) and (copiedObs['actual_warehouse'].disposition[0,c] == 0):
                            act.append(
                                {
                                    'type': 'P',
                                    'col1': col,
                                    'col2': c
                                }
                            )

                            copiedObs['actual_warehouse']._move(col,c)
                            break
            
            act.append(
                {'type': 'O', 'col': col, 'n_order': i}
            )
            copiedObs['actual_warehouse']._take(col)
            #print('order')
            #print(copiedObs['actual_warehouse'].disposition)
            
        # LOCATE NEW PARCELS
        for i, parcel in enumerate(copiedObs['new_parcel']):
            for col in range(copiedObs['actual_warehouse'].n_cols):
                if copiedObs['actual_warehouse'].disposition[0, col]==0:
                    act.append(
                        {'type': 'N', 'n_parcel': i, 'col': col}
                    )

                    copiedObs['actual_warehouse']._locate(
                        parcel,
                        col
                    )

                    #print('new item')
                    #print(copiedObs['actual_warehouse'].disposition)

                    break
                
        return act
    

    def learn(self, iterations = 10):
        pass
