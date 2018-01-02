"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch
"""
'''
ShuHo Chou schou33
'''
import datetime
import pandas as pd
import util as ut
import BagLearner as bl
import DTLearner as dt
import numpy as np
from indicators import exponential_moving_average, simple_moving_average, bollinger_band
from marketsimcode import marketsim
import random

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.window_size = 20
        self.feature_size = 5
        self.N = 10
        bag = 20
        leaf_size = 5
        self.learner = bl.BagLearner(learner=dt.DTLearner, bags=bag, kwargs={"leaf_size":leaf_size})
    def author():
        return 'schou33'

    def addEvidence(self, symbol = "IBM", \
        sd=datetime.datetime(2008,1,1), \
        ed=datetime.datetime(2009,1,1), \
        sv = 10000):


        window_size = self.window_size
        feature_size = self.feature_size
        # N day return
        N = self.N
        # threshold
        threshold = max(0.03, 2 * self.impact)

        prices = ut.get_data([symbol], pd.date_range(sd, ed))
        prices = prices[symbol]
        SMA = simple_moving_average(prices, window = window_size, show_pic = False)
        BB = bollinger_band(prices, window = window_size, show_pic = False)
        EMA = exponential_moving_average(prices, window = window_size, show_pic = False)

        X = []
        Y = []
        for i in range(window_size + feature_size + 1, len(prices) - N):
            # X will be a feature_size * 3 dimension data
            X.append( np.concatenate( (SMA[i - feature_size : i], BB[i - feature_size : i], EMA[i - feature_size : i]) ) )
            ret = (prices.values[i + N] - prices.values[i]) / prices.values[i]
            if ret > threshold:
                Y.append(1)
            elif ret < -threshold:
                Y.append(-1)
            else:
                Y.append(0)

        X = np.array(X)
        Y = np.array(Y)
        self.learner.addEvidence(X, Y)

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=datetime.datetime(2009,1,1), \
        ed=datetime.datetime(2010,1,1), \
        sv = 10000):

        current_holding = 0

        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        trades = prices_all[[symbol,]].copy(deep=True)  # only portfolio symbols
        trades_SPY = prices_all['SPY']  # only SPY, for comparison later

        window_size = self.window_size
        feature_size = self.feature_size

        prices = ut.get_data([symbol], pd.date_range(sd, ed))
        prices = prices[symbol]

        SMA = simple_moving_average(prices, window = window_size, show_pic = False)
        BB = bollinger_band(prices, window = window_size, show_pic = False)
        EMA = exponential_moving_average(prices, window = window_size, show_pic = False)

        trades.values[:, :] = 0
        Xtest = []
        for i in range(window_size + feature_size + 1, len(prices) - 1):
            data = np.concatenate( (SMA[i - feature_size : i], BB[i - feature_size : i], EMA[i - feature_size : i]) )
            Xtest.append(data)

        res = self.learner.query(Xtest)
        for i, r in enumerate(res):
            if r > 0:
                # Buy signal
                trades.values[i + window_size + feature_size + 1, :] = 1000 - current_holding
                current_holding = 1000
            elif r < 0:
                # Sell signal
                trades.values[i + window_size + feature_size + 1, :] = - 1000 - current_holding
                current_holding = -1000

        if self.verbose: print type(trades) # it better be a DataFrame!
        if self.verbose: print trades
        if self.verbose: print prices_all

        return trades

if __name__=="__main__":
    print "One does not simply think up a strategy"
