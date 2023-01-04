from env.grid import Grid
from env.warehouse import Warehouse


class ModifiedWarehouse(Warehouse):
    
    def __init__(self, numberOfParcelTypes, numberOfRows, numberOfColumns):
        Warehouse.__init__(self, numberOfParcelTypes, numberOfRows, numberOfColumns)

        self.actionList = []

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
        
        #initialize state graph
        self.stateGraph = StateGraph()

        initialState = self.disposition.disposition
        initialStateNode = StateNode()
        initialStateNode.state = initialState

        self.stateGraph.currentNode = initialStateNode 

        

class StateGraph:
    def __init__(self):
        self.currentNode = None

    def expand(self, actionList):
        pass       

class StateNode:
    def __init__(self):
        self.state = None
        self.links = []
        self.stateActionValue = []

class ActionLinks:
    def __init__(self):
        self.src = None
        self.dest = None
        self.action = None

