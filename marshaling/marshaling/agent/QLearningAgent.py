from agent.Agent import Agent
import random
import numpy as np
import copy

class QLearningAgent(Agent):
    def __init__(self, startQTable, alpha, gamma, epsilon):
        print("QLearningAgent::__init__")
        self.qTable = startQTable
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.count=0

    def get_action(self, obs, env):
        print("QLearningAgent::get_action")
        actionList = []

        #TO BE IMPLEMENTED: reorganize the warehouse
        virtualEnv = copy.deepcopy(env)
        for i in range(0,4):
            state = virtualEnv.disposition.disposition
            encodedState = virtualEnv.encodeState(state)
            encodedAction = np.argmax(self.qTable[encodedState])
            action_index = virtualEnv.actionList[encodedAction]
            virtualEnv.step([action_index])
            actionList.append(action_index)
            

        act = Agent.get_action(obs)

        return actionList.append(act)

    #env: training environment
    #this method is evoked when we train our agent to achieve optimal action_value function (qTable)
    #some env methods need implementing
    def learn(self, env):
        print("QLearningAgent::learn")
        state = env.returnRandomState()

        print(env.stateList[state])
        
        done = False
        self.count+=1
        iterations=0
        while not done and iterations<=1000:
            
            print(f"episode{self.count}")
            print(f'iteration:{iterations}')

            if random.uniform(0,1) < self.epsilon:
                print("explore")
                feasibleActions = env.getFeasibleActions()
                if len(feasibleActions) == 0:
                    return
                randomIndex = random.randint(0, len(feasibleActions) - 1)
                action_index = feasibleActions[randomIndex] #explore the action_index space
            else:
                print("exploit")
                feasibleActions = env.getFeasibleActions()
                if len(feasibleActions) == 0:
                    return
                action_index = feasibleActions[np.argmax(self.qTable[state, feasibleActions])]#exploit learned values
                print(action_index)

            if len(feasibleActions) == 0 or action_index==-1 :
                return
            nextState, reward, done  = env.stepLearn(action_index) 

            oldValue = self.qTable[state, action_index]
            nextMax = np.max(self.qTable[nextState])
            
            new_value = (1 - self.alpha) * oldValue + self.alpha * (reward + self.gamma * nextMax)
            self.qTable[state, action_index] = new_value

            state = nextState
            iterations+=1
            print(env.stateList[state])
    

        


       
