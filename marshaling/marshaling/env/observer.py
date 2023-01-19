import copy
import numpy as np
from scipy.stats import poisson
from collections import Counter

class Observer:
    def __init__(self):
        print('Observer::__init__')
        self.parcelTypes = [1,2,3,4]
        self.probabilityOfOrder = [0.6, 0.3, 0.08, 0.02]


    def getObservation(self, grid):

        #numberOfNewParcels = poisson.rvs(0.2,1)
        #numberOfOrders = poisson.rvs(0,2,1)
        numberOfNewParcels = 2
        numberOfOrders = 2



        #observe orders
        orders = []

        #find coordinates of current parcels
        coordinates = np.transpose(np.nonzero(grid.disposition))

        #get current parcels in the warehouse
        currentParcels = []
        for coordinate in coordinates:
            currentParcels.append(grid.disposition[coordinate[0], coordinate[1]])

        for i in range(0, numberOfOrders):
            orderedParcel = np.random.choice(a=self.parcelTypes,p= self.probabilityOfOrder)

            while orderedParcel not in currentParcels:
                orderedParcel = np.random.choice(a=self.parcelTypes,p= self.probabilityOfOrder)
            
            orders.append(orderedParcel)
        
        #observe new parcels
        newParcels = []

        for i in range(0, numberOfNewParcels):
            parcel = np.random.randint(low = 1, high = 4)
            newParcels.append(parcel)
        
        obs = {
            'actual_warehouse' : copy.deepcopy(grid),
            'order' : orders,
            'new_parcel' : newParcels
        }

        return obs








        


