import numpy as np

# Bootstrap Aggregating Learner
class BagLearner():
    def __init__(self, learner, kwargs={}, bags=20, boost=False, verbose=False):
        self.learners = []
        for i in range(bags):
            self.learners.append(learner(**kwargs))
        self.bags = bags
        self.kwargs = kwargs
        self.boost = boost
        self.verbose = verbose

    def author(self):
        return 'schou33'

    # add training data and train
    def addEvidence(self, Xtrain, Ytrain):
        for learner in self.learners:
            indices = np.random.randint(Xtrain.shape[0], size=Xtrain.shape[0])
            learner.addEvidence(Xtrain[indices], Ytrain[indices])

    def query(self, Xtest):
        val = 0.0
        for learner in self.learners:
            val += learner.query(Xtest)
        return val / self.bags
