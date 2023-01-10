import copy
import itertools
import numpy as np
from env.grid import Grid
from env.warehouse import Warehouse
from gym.spaces import Box, Discrete


class ModifiedWarehouse(Warehouse):
    
    def __init__(self, numberOfParcelTypes, numberOfRows, numberOfColumns):
        print("ModifiedWarehouse::__init__")
        Warehouse.__init__(self, numberOfParcelTypes, numberOfRows, numberOfColumns)

        #a list to store all the states
        self.actionList = []
        #a list to store all the actions
        self.stateList = []

        #this is used to generate random state
        self.stateSpace = Box(low= 0, high= self.n_parcel_types, shape=(self.n_rows,self.n_cols), dtype = int)
        #this is used to generate random action
        self.actionSpace = Discrete(self.n_cols * (self.n_cols - 1))

        #populate the action list
        for fromColumn in range(0, self.n_cols):
            for toColumn in range(0, self.n_cols):
                if fromColumn != toColumn:
                    action = {'type': 'P', 'col1': fromColumn, 'col2': toColumn}
                    self.actionList.append(action)

        #populate the state list
        for state in itertools.product(range(0, self.n_parcel_types + 1), repeat = self.n_cols * self.n_rows):
            state = np.array(state)
            state = state.reshape((self.n_rows, self.n_cols))

            self.stateList.append(state)

    def reset(self):
        print("ModifiedWarehouse::reset")
        self.disposition.disposition = self.stateSpace.sample()
        obs = self._get_obs()
        
        return obs
        
    def returnRandomState(self):
        print("ModifiedWarehour::returnRandomState")
        notValid = True

        while notValid:
            obs = self.reset()
            sampleState = obs['actual_warehouse'].disposition
            notValid = self.validate(sampleState)
        
        encodedState = self.encodeState(sampleState)

        return encodedState
    
    def validate(self, state):
        print("ModifiedWarehouse::validate")
        for row in range(0, self.n_rows-1):
            for col in range(0, self.n_cols):
                if (state[row, col] != 0) and (state[row+1, col] == 0):
                    return True
        
        return False

    
    def encodeState(self, state):
        print("ModifiedWarehouse::encodeState")
        print(state)
        for i, s in enumerate(self.stateList):
            print(s)
            if np.array_equal(state, s):
                print(s)
                return i
        
        return -1 
    
    def decodeState(self, code):
        print("ModifiedWarehouse::decodeState")
        return self.stateList[code]


    def stepLearn(self, action):
        print("ModifiedWarehouse::stepLearn")
        #decode action
        action = self.actionList[action]

        #execute the action
        #ignore the cost and infor
        #only obs is useful to determine new state
        obs, cost, infor = Warehouse.step([action])

        nextState = self.encodeState(obs['actual_warehouse'].disposition)
        reward = self.evaluateState(obs['actual_warehouse'].disposition)
        done = self.isFinished(obs['actual_warehouse'].disposition)

        return nextState, reward, done


    def evaluateState(self, state):
        print("ModifiedWarehouse::evaluateState")
        totalReward = 0

        for col in range(0, self.n_cols):
            reward = 0
            for row in range(0, self.n_rows - 1):
                if state[row, col] < state[row+1, col]:
                    reward = reward + 1
            
            totalReward = totalReward + reward
        return totalReward

    def isFinished(self, state):
        print("ModifiedWarehouse::isFinished")
        for col in range(0, self.n_cols):
            for row in range(0, self.n_rows - 1):
                if state[row, col] > state[row+1, col]:
                    return False
        
        return True










        


        


            









