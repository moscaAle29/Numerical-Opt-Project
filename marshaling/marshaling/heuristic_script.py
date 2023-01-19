from agent.HeuristicAgent import HeuristicAgent
from agent.Agent import Agent
from env.warehouse import Warehouse2
from env.Observer import Observer
import numpy as np

timeLimit = 500

#define warehouse
numberOfColumns = 3
numberOfRows = 3
numberOfParcelTypes = 4

initialState = np.array([[0,0,0],[4,4,0],[1,2,3]])

observer = Observer()

heuristicWarehouse = Warehouse2(numberOfParcelTypes, numberOfRows, numberOfColumns)
naiveWarehouse = Warehouse2(numberOfParcelTypes, numberOfRows, numberOfColumns)

#2 Agents
heuristicAgent = HeuristicAgent(env=heuristicWarehouse)
naiveAgent = Agent()

#set inital state for both warehouses
heuristicWarehouse.disposition.disposition = initialState
naiveWarehouse.disposition.disposition = initialState

heuristicCost = 0
naiveCost = 0

obs = observer.getObservation(naiveWarehouse.disposition)

for t in range(timeLimit):
    #naive approach
    naiveWarehouse.orders = obs['order']
    naiveWarehouse.new_parcels = obs['new_parcel']
    action = naiveAgent.get_action(obs)
    cost = naiveWarehouse.step(action)
    naiveCost += cost
    print(naiveWarehouse.disposition.disposition)
    print("-------------------------------------")

    #heuristic approach
    heuristicWarehouse.orders = obs['order']
    heuristicWarehouse.new_parcels = obs['new_parcel']    
    action = heuristicAgent.get_action(obs)
    cost = heuristicWarehouse.step(action)
    heuristicCost += cost
    print(heuristicWarehouse.disposition.disposition)

    obs = observer.getObservation(naiveWarehouse.disposition)

print(f'naive:         {naiveCost}')
print(f'heuristic:      {heuristicCost}')





