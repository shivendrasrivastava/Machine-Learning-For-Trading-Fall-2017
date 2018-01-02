import numpy as np

class RTLearner():
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
        if self.verbose:
            print tree

    def buildtree(self, data):
        Xtrain = data[:, :-1]
        Ytrain = data[:, -1]
        if data.shape[0] <= self.leaf_size:
            return np.array([[self.LEAF, Ytrain.mean(), self.NA, self.NA]])
        if np.std(Ytrain) == 0.0:
            return np.array([[self.LEAF, Ytrain.mean(), self.NA, self.NA]])

        # Rather than using correlation as metric, randomly pick a factor
        factor = np.random.randint(Xtrain.shape[1])

        # Rather than choose median, simply choose two random values in that factor, and take the mean

        random_split = (Xtrain[np.random.randint(Xtrain.shape[0]), factor] + Xtrain[np.random.randint(Xtrain.shape[0]), factor]) / 2.0
        data_left = data[data[:, factor] <= random_split]
        data_right = data[data[:, factor] > random_split]
        if data_right.shape[0] == 0:
            flag = True
            # Let it try three more times, if still not separable, confident enough to say it's a leaf.
            for i in range(3):
                random_split = (Xtrain[np.random.randint(Xtrain.shape[0]), factor] + Xtrain[np.random.randint(Xtrain.shape[0]), factor]) / 2.0
                data_left = data[data[:, factor] <= random_split]
                data_right = data[data[:, factor] > random_split]
                if data_right.shape[0] != 0:
                    flag = False
                    break
            if flag:
                return np.array([[self.LEAF, Ytrain.mean(), self.NA, self.NA]])

        left = self.buildtree(data_left)
        right = self.buildtree(data_right)
        root = np.array([[factor, random_split, 1, left.shape[0] + 1]])
        root = np.concatenate((root, left, right))
        return root


    def query(self, Xtest):
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
        # print Y
        return np.array(Y)
