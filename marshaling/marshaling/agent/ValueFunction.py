from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
class ValueFunction:
    def __init__(self):
        pass

class AVF(ValueFunction):
    def __init__(self):
        #self.model = make_pipeline(PolynomialFeatures(2), LinearRegression())
        #self.model = RandomForestRegressor()
        self.model = LinearRegression(fit_intercept = True)
        #self.model = KNeighborsRegressor()
        #self.model = make_pipeline(StandardScaler(), MLPRegressor())

    def transform(self, state):
        numberOfRows = state.shape[0]
        numberOfColumns = state.shape[1]

        instance = []
        for i in range(0, numberOfRows):
            w = sum(state[i,:])
            #instance.append(w)
        
        for c in range(0, numberOfColumns):
            v = 0
            for r in range(0, numberOfRows -1):
                if state[r, c] <= state[r+1,c]:
                    v = v + 1

            #instance.append(v)
        
        for c in range(0, numberOfColumns):
            for r in range(0, numberOfRows):
                s = state[r, c]
                instance.append(s)
        
        #for r in range(0, numberOfRows):
        #    z = 0
        #    for c in range(0, numberOfColumns):
        #        if state[r,c] ==0:
        #            z = z + 1
            
        #    instance.append(z)


        return instance 

    def update(self, X, y):
        self.model.fit(X,y)

    def cal(self, state):
        instance = self.transform(state)
        
        return self.model.predict([instance])

class AVF2(AVF):
    def cal(self, state):
        w = super().transform(state)
        
        return sum(w)

class AVF3():
    def cal(self, state):
        numberOfRows = state.shape[0]
        numberOfColumns = state.shape[1]

        value = 0

        for col in range(0, numberOfColumns):
            for row in range(0, numberOfRows - 1):
                if state[row, col] != 0:
                    if state[row,col] <= state[row + 1,col]:
                        value = value + 10
                    else:
                        value = value - 10
        
        return value
