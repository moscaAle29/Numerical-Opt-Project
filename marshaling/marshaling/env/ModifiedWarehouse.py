import copy
import itertools
import numpy as np
from env.grid import Grid
from env.warehouse import Warehouse
from gym.spaces import Box, Discrete


class ModifiedWarehouse(Warehouse):
    
    def __init__(self, numberOfParcelTypes, numberOfRows, numberOfColumns):
        print("ModifiedWarehouse::__init__")
        self.warehouse=Warehouse.__init__(self, numberOfParcelTypes, numberOfRows, numberOfColumns)

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
        valid = False
        while not valid:
            self.disposition.disposition = self.stateSpace.sample()
            valid = self.validate(self.disposition.disposition)

        #create empty col
        for i in range(0, self.n_rows):
            self.disposition.disposition[i, self.n_cols - 1] = 0

        obs = self._get_obs()
        
        return obs
        
    def returnRandomState(self):
        print("ModifiedWarehour::returnRandomState")

        obs = self.reset()
        sampleState = obs['actual_warehouse'].disposition
        encodedState = self.encodeState(sampleState)

        return encodedState
    
    def validate(self, state):
        print("ModifiedWarehouse::validate")
        for row in range(0, self.n_rows-1):
            for col in range(0, self.n_cols):
                if (state[row, col] != 0) and (state[row+1, col] == 0):
                    return False
        
        return True

    
    def encodeState(self, state):
        print("ModifiedWarehouse::encodeState")
        for i, s in enumerate(self.stateList):
            if np.array_equal(state, s):
                return i
        
        return -1 
    
    def decodeState(self, code):
        print("ModifiedWarehouse::decodeState")
        return self.stateList[code]


    def stepLearn(self, action):
        print("ModifiedWarehouse::stepLearn")
        #decode action
        action_list = [self.actionList[action]]

        #currentStateValue = self.evaluateState(self.disposition.disposition)

        #execute the action
        #ignore the cost and infor
        #only obs is useful to determine new state
        obs, cost, infor = Warehouse.step(self,action = action_list)

        #nextStateValue = self.evaluateState(obs['actual_warehouse'].disposition)

        nextState = self.encodeState(obs['actual_warehouse'].disposition)
        reward = -1
        done = self.isFinished(obs['actual_warehouse'].disposition)

        if done == True:
            reward = reward + 1000

        return nextState, reward, done


    def evaluateState(self, state):
        print("ModifiedWarehouse::evaluateState")
        totalReward = 0

        for col in range(0, self.n_cols):
            reward = 0
            for row in range(0, self.n_rows - 1):
                if (state[row, col] != 0) and (state[row, col] <= state[row+1, col]):
                    reward = reward + 1
            
            totalReward = totalReward + reward

         
        return totalReward

    def isFinished(self, state):
        print("ModifiedWarehouse::isFinished")
        #the high priority item must be on top of the low priority item
        for col in range(0, self.n_cols):
            for row in range(0, self.n_rows - 1):
                if state[row, col] > state[row+1, col]:
                    return False
        
        #the extra col must be empty in the end
        #if state[self.n_rows - 1, self.n_cols - 1] != 0:
        #    return False
        
        return True

    def validateAction(self,  encodedAction):
        action = self.actionList[encodedAction]
        
        grid= copy.deepcopy(self.disposition)
        
        result = grid._move(action["col1"], action["col2"])
        
        if result == -1:
            return False
        else:
            return True
        
    def getRandomAction(self):
        valid = False
        
        #check for number of elements => unfeasible=>return -1
                
        while not valid:
            encodedAction = self.actionSpace.sample()
            valid = self.validateAction(encodedAction)
            
        return encodedAction

    def getFeasibleActions(self):
        feasibleActionList = []
        for i, action in enumerate(self.actionList):
            grid = copy.deepcopy(self.disposition)
            
            if grid._move(action["col1"], action["col2"]) != -1 :
                feasibleActionList.append(i)
        
        return feasibleActionList