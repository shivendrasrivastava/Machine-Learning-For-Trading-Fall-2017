# Code implementing a BestPossibleStrategy object (details below). It should implement testPolicy() which returns a
# trades data frame (see below). The main part of this code should call marketsimcode as necessary to generate the plots used in the report.
import pandas as pd
import numpy as np
import math
import datetime as dt
import types
import os
import matplotlib.pyplot as plt
from util import get_data, plot_data
from marketsimcode import marketsim

# Input:
#
# Return:
#   data frame fo trades --> df_trades
# def testPolicy(prices):
def testPolicy(symbol = 'JPM', sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31), sv = 100000):
    prices = get_data([symbol], pd.date_range(sd, ed))
    prices = prices[symbol]
    df_trades = pd.DataFrame(data=np.zeros(len(prices.index)), index=prices.index, columns = ['val'])
    nums = prices.values

    # Initialize at position 0
    INCREASING = nums[1] > nums[0]
    df_trades['val'].iloc[0] = 1000 * (1 if INCREASING else -1)

    for i in range(1, len(nums) - 1):
        if (nums[i] < nums[i + 1] and not INCREASING) or (nums[i] >= nums[i + 1] and INCREASING):
            INCREASING = not INCREASING
            df_trades['val'].iloc[i] = 2000 * (1 if INCREASING else -1)

        # if nums[i - 1] < nums[i] and not INCREASING:
        #     INCREASING = not INCREASING
        #     df_trades['val'].iloc[i - 1] = 2000
        # elif nums[i - 1] >= nums[i] and INCREASING:
        #     INCREASING = not INCREASING
        #     df_trades['val'].iloc[i - 1] = -2000

    return df_trades

def print_info(portvals):
    portvals = portvals / portvals.ix[0]
    daily_returns = portvals / portvals.shift(1) - 1
    daily_returns = daily_returns[1:]

    print 'cumulative return: ' + str(float(portvals.values[-1] / portvals.values[0]) - 1)
    print 'Stdev of daily returns: ' + str(float(daily_returns.std()))
    print 'Mean of daily returns: ' + str(float(daily_returns.mean()))

if __name__ == '__main__':
    names = ['JPM']
    start_date = '2008-01-01'
    end_date = '2009-12-31'
    prices = get_data(names, pd.date_range(start_date, end_date))
    prices = prices[names]

    df_trades = testPolicy()
    portvals = marketsim(df_trades, prices)
    print 'Best Possible Policy'
    print_info(portvals)

    d = np.zeros(len(prices.index))
    d[0] = 1000
    df_trade_none = pd.DataFrame(data=d, index=prices.index, columns = ['val'])
    port_benchmark = marketsim(df_trade_none, prices)
    print 'Benchmark'
    print_info(port_benchmark)

    portvals = portvals / portvals.ix[0]
    port_benchmark = port_benchmark / port_benchmark.ix[0]
    # df_joined = portvals.join(port_benchmark, lsuffix='_best', rsuffix='_benchmark')
    # plot_data(df_joined)

    benchmark, = plt.plot(port_benchmark, 'b')
    best, = plt.plot(portvals, 'k')
    plt.legend([benchmark, best], ['Benchmark', 'Best'])
    plt.ylabel('Normalized Price')
    plt.xlabel('Date')
    plt.show()
