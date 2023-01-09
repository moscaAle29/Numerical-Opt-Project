import copy
import itertools
import numpy as np
from env.grid import Grid
from env.warehouse import Warehouse
from gym.spaces import Box


class ModifiedWarehouse(Warehouse):
    
    def __init__(self, numberOfParcelTypes, numberOfRows, numberOfColumns):
        Warehouse.__init__(self, numberOfParcelTypes, numberOfRows, numberOfColumns)

        self.actionList = []
        self.stateList = []
        self.sampleGenerator = Box(low= 0, high= self.n_parcel_types + 1, shape=(self.n_rows,self.n_cols), dtype = int)

        """
        #add actions type P & type O
        for fromColumn in range(0, self.n_cols):
            for toColumn in range(0, self.n_cols):
                if fromColumn == toColumn:
                    for parcelType in range(1, self.n_parcel_types + 1):
                        action = {'type': 'O', 'col': fromColumn, 'parcelType': parcelType}
                        self.actionList.append(action)
                else:
                    action = {'type': 'P', 'col1': fromColumn, 'col2': toColumn}
                    self.actionList.append(action)
        
        #add actions type N
        for selectedColumn in range(0, self.n_cols):
            for parcelType in range(1, self.n_parcel_types + 1):
                action = {'type': 'N', 'col': selectedColumn, 'parcelType': parcelType}
                self.actionList.append(action) 
        """

        for fromColumn in range(0, self.n_cols):
            for toColumn in range(0, self.n_cols):
                if fromColumn != toColumn:
                    action = {'type': 'P', 'col1': fromColumn, 'col2': toColumn}
                    self.actionList.append(action)

        
        for state in itertools.combinations_with_replacement(range(0, self.n_parcel_types + 1), self.n_cols * self.n_rows):
            state = np.array(state)
            state = state.reshape((self.n_rows, self.n_cols))

            self.actionList.append(state)
        
    def reset(self):
        notValid = True
        while notValid:
            sampleState = self.sampleGenerator().sample()
            notValid = self.validate(sampleState)
        
        encodedState = self.encoded(sampleState)
    
    def validate(self, state):
        for row in range(0, self.n_rows-1):
            for col in range(0, self.n_cols):
                if (state[row, col] != 0) and (state[row+1, col] == 0):
                    return False
        
        return True

    
    def encoded(self, state):
        pass









        


        


            









