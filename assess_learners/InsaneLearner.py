import LinRegLearner as ll
import BagLearner as bl

# Insane Learner generates a BAG of 20 linear regression learner
# with few lines
class InsaneLearner(bl.BagLearner):
    def __init__(self, verbose=False):
        self.learners = [bl.BagLearner(learner=ll.LinRegLearner, bags=20) for i in range(20)]
        self.bags = 20
