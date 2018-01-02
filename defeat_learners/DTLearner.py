import numpy as np
import time

class DTLearner():
    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = []
        self.LEAF = -1;
        self.NA = -1;

    def author(self):
        return 'schou33'

    def addEvidence(self, Xtrain, Ytrain):
        Ytrain = np.array([Ytrain])
        data = np.concatenate((Xtrain, Ytrain.T), axis=1)

        tree = self.buildtree(data)
        self.tree = tree


    def buildtree(self, data):
        Xtrain = data[:, :-1]
        Ytrain = data[:, -1]
        if data.shape[0] <= self.leaf_size:
            return np.array([[self.LEAF, Ytrain.mean(), self.NA, self.NA]])

        corrs = np.array([abs(np.corrcoef(Xtrain[:, x], Ytrain)[0][1]) for x in range(Xtrain.shape[1])])
        corrs[np.isnan(corrs)] = 0

        factor = np.argmax(corrs)
        median = np.median(Xtrain[:, factor])

        data_right = data[data[:, factor] > median]
        data_left = data[data[:, factor] <= median]

        # Here if all data goes to left, I first minus the median by a very small value
        # and see if it split well, if this time all the data go to the left side, then
        # I know that they all have the same values, so it should be a leaf.
        if data_right.shape[0] == 0:
            median -= 0.00001
            data_right = data[data[:, factor] > median]
            data_left = data[data[:, factor] <= median]
            if data_left.shape[0] == 0:
                return np.array([[self.LEAF, Ytrain.mean(), self.NA, self.NA]])

        left = self.buildtree(data_left)
        right = self.buildtree(data_right)
        root = np.array([[factor, median, 1, left.shape[0] + 1]])
        root = np.concatenate((root, left, right))
        return root


    def query(self, Xtest):
        if self.verbose:
            print self.tree
        Y = []
        for x in Xtest:
            idx = 0
            while True:
                factor = int(self.tree[idx][0])
                # Reached Leaf
                if factor == self.LEAF:
                    Y.append(self.tree[idx][1])
                    break
                # Go left
                if x[factor] <= self.tree[idx][1]:
                    idx += int(self.tree[idx][2])
                else:
                    idx += int(self.tree[idx][3])
        return np.array(Y)

# """
# A simple wrapper for linear regression.  (c) 2015 Tucker Balch
# Note, this is NOT a correct DTLearner; Replace with your own implementation.
# """
#
# import numpy as np
# import warnings
#
# class DTLearner(object):
#
#     def __init__(self, leaf_size=1, verbose = False):
#         warnings.warn("\n\n  WARNING! THIS IS NOT A CORRECT DTLearner IMPLEMENTATION! REPLACE WITH YOUR OWN CODE\n")
#         pass # move along, these aren't the drones you're looking for
#
#     def author(self):
#         return 'tb34' # replace tb34 with your Georgia Tech username
#
#     def addEvidence(self,dataX,dataY):
#         """
#         @summary: Add training data to learner
#         @param dataX: X values of data to add
#         @param dataY: the Y training values
#         """
#
#         # slap on 1s column so linear regression finds a constant term
#         newdataX = np.ones([dataX.shape[0],dataX.shape[1]+1])
#         newdataX[:,0:dataX.shape[1]]=dataX
#
#         # build and save the model
#         self.model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX, dataY)
#
#     def query(self,points):
#         """
#         @summary: Estimate a set of test points given the model we built.
#         @param points: should be a numpy array with each row corresponding to a specific query.
#         @returns the estimated values according to the saved model.
#         """
#         return (self.model_coefs[:-1] * points).sum(axis = 1) + self.model_coefs[-1]
#
# if __name__=="__main__":
#     print "the secret clue is 'zzyzx'"
