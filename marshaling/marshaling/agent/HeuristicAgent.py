import copy
from agent.Agent import Agent
from agent.ValueFunction import AVF, AVF2, AVF3
import itertools
import numpy as np

class HeuristicAgent(Agent):
    def __init__(self, env):
        #Approximate Value Function
        self.V = AVF()

        #s1 = np.array([[0,0,0],[4,4,0],[1,2,3]])
        #s2 = np.array([[0,0,0],[1,3,0],[4,4,2]])
        #s3 = np.array([[0,0,0],[1,2,0],[4,4,3]])  
        #s4 = np.array([[0,0,0],[4,3,0],[4,2,1]])
        #s5 = np.array([[0,0,0],[1,4,0],[4,3,2]])
        #self.V.update([self.V.transform(s1),self.V.transform(s2),self.V.transform(s3),self.V.transform(s4),self.V.transform(s5)],[-2,2,2,2,1])

        self.time = 0
        self.alpha = 0.2

        self.X = []
        self.y = []
        self.S_prev = None

        #get information of the env
        numberOfColumns = env.n_cols
        numberOfMoves = numberOfColumns * (numberOfColumns - 1)

        #define move
        self.moveList = []
        for fromColumn in range(0, numberOfColumns):
            for toColumn in range(0, numberOfColumns):
                if fromColumn != toColumn:
                    move = {'type': 'P', 'col1': fromColumn, 'col2': toColumn}
                    self.moveList.append(move)
        #define action
        self.actionList = []
        for action in itertools.product(range(-1,numberOfMoves), repeat=4):
            self.actionList.append(action)

    def get_action(self, obs):
        #find v^_t: value
        bestValue = None
        bestAction = None
        bestVirtualGrid = None

        for action in self.actionList:
            virtualGrid = copy.deepcopy(obs['actual_warehouse'])
            virtualGrid.disposition = obs['actual_warehouse'].disposition.copy()
            totCost = 0
            unfeasibleAction = False
            for moveIndex in action:
                if (moveIndex == -1):
                    continue

                move = self.moveList[moveIndex]

                #if the move is not possible, break the loop and discard the action
                if virtualGrid._move(move['col1'], move['col2']) == -1:
                    unfeasibleAction = True
                    break

                totCost = totCost + 1
            
            if unfeasibleAction == True:
                continue

            value = totCost + float(self.V.cal(virtualGrid.disposition))

            if bestValue == None:
                bestValue = value
                bestAction = action
                bestVirtualGrid = virtualGrid
            else:
                if value < bestValue:
                    bestValue = value
                    bestAction = action
                    bestVirtualGrid = virtualGrid
            
        #update the value function
        if (self.time % 100) == 0:
            self.S_prev = bestVirtualGrid.disposition
            self.time = self.time + 1
        else:
            x = self.V.transform(self.S_prev)
            self.X.append(x)
            newValue = (1-self.alpha) * float(self.V.cal(self.S_prev)) + self.alpha * bestValue
            self.y.append(newValue)

            #end an episode
            if self.time % 100 == 99:
                self.V.update(self.X, self.y)
        
                self.X = []
                self.y = []
                self.S_prev = None
        
            self.time = self.time + 1
        


        #generate list of moves = action
        moveList = []
        for moveIndex in bestAction:
            if moveIndex != -1:
                moveList.append(self.moveList[moveIndex])
        
        #update observation
        newObs = {
            'actual_warehouse' : bestVirtualGrid,
            'order' : obs['order'],
            'new_parcel' : obs['new_parcel']
        }

        extraMoves = super().get_action(newObs)

        moveList.extend(extraMoves)

        return moveList


    def learn(self, obs):
        pass

