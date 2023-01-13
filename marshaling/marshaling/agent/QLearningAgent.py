from agent.agent import Agent
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

    def get_action(self, obs, env):
        print("QLearningAgent::get_action")
        actionList = []

        #TO BE IMPLEMENTED: reorganize the warehouse
        virtualEnv = copy.deepcopy(env)
        for i in range(0,10):
            state = virtualEnv.disposition.disposition
            encodedState = virtualEnv.encodeState(state)
            encodedAction = np.argmax(self.qTable[encodedState])
            action = virtualEnv.actionList[encodedAction]
            virtualEnv.step([action])
            actionList.append(action)
            

        act = Agent.get_action(obs)

        return actionList.append(act)

    #env: training environment
    #this method is evoked when we train our agent to achieve optimal action_value function (qTable)
    #some env methods need implementing
    def learn(self, env):
        print("QLearningAgent::learn")
        state = env.returnRandomState()

        print(state)
        
        done = False

        while not done:
            if random.uniform(0,1) < self.epsilon:
                print("explore")
                action = env.getRandomAction() #explore the action space
            else:
                print("exploit")
                feasibleActions = env.getFeasibleActions()
                action = np.argmax(self.qTable[state, feasibleActions]) #exploit learned values
                print(action)

        nextState, reward, done  = env.stepLearn(action) 

        oldValue = self.qTable[state, action]
        nextMax = np.max(self.qTable[nextState])
        
        new_value = (1 - self.alpha) * oldValue + self.alpha * (reward + self.gamma * nextMax)
        self.qTable[state, action] = new_value

        state = nextState

