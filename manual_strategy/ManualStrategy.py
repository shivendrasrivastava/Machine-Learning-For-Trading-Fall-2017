# Code implementing a ManualStrategy object (your manual strategy).
# It should implement testPolicy() which returns a trades data frame (see below).
# The main part of this code should call marketsimcode as necessary to generate the plots
# used in the report.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import datetime as dt
import types
import os
from util import get_data, plot_data
from marketsimcode import marketsim
from indicators import exponential_moving_average, simple_moving_average, bollinger_band

def print_info(portvals):
    portvals = portvals / portvals.ix[0]
    daily_returns = portvals / portvals.shift(1) - 1
    daily_returns = daily_returns[1:]

    print 'cumulative return: ' + str(float(portvals.values[-1] / portvals.values[0]) - 1)
    print 'Stdev of daily returns: ' + str(float(daily_returns.std()))
    print 'Mean of daily returns: ' + str(float(daily_returns.mean()))


def testPolicy(symbol = 'JPM', sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31), sv = 100000):
    prices = get_data([symbol], pd.date_range(sd, ed))
    prices = prices[symbol]
    df_trades = pd.DataFrame(data=np.zeros(len(prices.index)), index=prices.index, columns = ['val'])

    current = 0
    my_window = 20
    BB = bollinger_band(prices, window = my_window, show_pic = False)
    SMA = simple_moving_average(prices, window = my_window, show_pic = False)
    EMA = exponential_moving_average(prices, window = my_window, show_pic = False)
    # print [x for x in BB if x > 1 or x < -1]
    for i in range(my_window, len(prices.index)):

        # if BB[i] < -1 and prices.values[i - 1] < prices.values[i]:
        #     df_trades['val'].iloc[i] = 1000 - current
        #     current = 1000
        # # elif abs(SMA[i]) < 0.01:
        # #     df_trades['val'].iloc[i] = -current
        # #     current = 0
        # elif BB[i] > 1 and prices.values[i - 1] > prices.values[i]:
        #     df_trades['val'].iloc[i] = - current - 1000
        #     current = -1000
        if SMA[i] < -0.1:
            df_trades['val'].iloc[i] = 1000 - current
            current = 1000
        elif SMA[i] > 0.1:
            df_trades['val'].iloc[i] = - current - 1000
            current = -1000

    return df_trades

if __name__ == '__main__':
    names = ['JPM']
    start_date = '2008-01-01'
    end_date = '2009-12-31'
    # start_date = '2010-01-01'
    # end_date = '2011-12-31'
    prices = get_data(names, pd.date_range(start_date, end_date))
    prices = prices[names]
    # print prices
    df_trades = testPolicy(sd=start_date, ed=end_date)
    df_joined = df_trades.join(prices, lsuffix='_best', rsuffix='_benchmark')

    portvals = marketsim(df_trades, prices, commission = 9.95, impact = 0.)
    # portvals = marketsim(df_trades, prices, commission = 0, impact = 0)
    df_joined = df_joined.join(portvals, lsuffix='_best', rsuffix = 'whatever')
    prices_val = prices.values

    # Benchmark
    d = np.zeros(len(prices.index))
    d[0] = 1000
    df_trade_none = pd.DataFrame(data=d, index=prices.index, columns = ['val'])
    port_benchmark = marketsim(df_trade_none, prices)

    portvals = portvals / portvals.ix[0]
    port_benchmark = port_benchmark / port_benchmark.ix[0]

    # ma, = plt.plot(moving_avg, 'r')
    # pr, = plt.plot(prices, 'g')
    benchmark, = plt.plot(port_benchmark, 'b')
    mystrategy, = plt.plot(portvals, 'k')
    for i in range(len(prices.index)):
        if df_trades['val'].iloc[i] > 0:
            plt.axvline(x=prices.index[i], c = 'g')
        elif df_trades['val'].iloc[i] < 0:
            plt.axvline(x=prices.index[i], c = 'r')

    plt.legend([benchmark, mystrategy], ['Benchmark', 'My strategy'])
    plt.show()


    print_info(portvals)
    print_info(port_benchmark)
