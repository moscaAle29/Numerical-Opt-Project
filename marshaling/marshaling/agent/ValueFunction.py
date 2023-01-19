from sklearn.linear_model import LinearRegression
class ValueFunction:
    def __init__(self):
        pass

class AVF(ValueFunction):
    def __init__(self):
        self.model = LinearRegression(fit_intercept = True)

    def transform(self, state):
        numberOfRows = state.shape[0]

        instance = []
        for i in range(0, numberOfRows):
            w = sum(state[i,:]) ** (numberOfRows - i)
            instance.append(w)

        return instance 

    def update(self, X, y):
        self.model.fit(X,y)

    def cal(self, state):
        instance = self.transform(state)
        
        return self.model.predict([instance])
