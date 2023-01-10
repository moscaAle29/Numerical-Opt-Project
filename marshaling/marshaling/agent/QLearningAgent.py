from agent.agent import Agent
import random
import numpy as np

class QLearningAgent(Agent):
    def __init__(self, startQTable, alpha, gamma, epsilon):
        self.qTable = startQTable
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_action(self, obs, env):
        actionList = []

        #TO BE IMPLEMENTED: reorganize the warehouse

        act = Agent.get_action(obs)

        return actionList.append(act)

    #env: training environment
    #this method is evoked when we train our agent to achieve optimal action_value function (qTable)
    #some env methods need implementing
    def learn(self, env):
        state = env.returnRandomState()
        
        done = False

        while not done:
            if random.uniform(0,1) < self.epsilon:
                action = env.actionSpace.sample() #explore the action space
            else:
                action = np.argmax(self.qTable[state]) #exploit learned values

        nextState, reward, done  = env.stepLearn(action) 

        oldValue = self.qTable[state, action]
        nextMax = np.max(self.qTable[nextState])
        
        new_value = (1 - self.alpha) * oldValue + self.alpha * (reward + self.gamma * nextMax)
        self.qTable[state, action] = new_value

        state = nextState

