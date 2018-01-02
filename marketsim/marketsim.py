"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import math
import datetime as dt
import types
import os
from util import get_data, plot_data

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    f = None
    if type(orders_file) == types.FileType:
        f = orders_file
    elif type(orders_file) == types.StringType:
        f = open(orders_file, 'r')
    else:
        print 'This should not happen'

    cash = start_val
    order_df = pd.read_csv(f, index_col='Date', parse_dates=True)

    order_df.sort_index(inplace=True)

    names = list(set(order_df['Symbol']))

    start_date = order_df.index[0]
    end_date = order_df.index[-1]
    prices = get_data(names, pd.date_range(start_date, end_date))
    prices = prices[names]  # remove SPY
    portvals = pd.DataFrame(data=np.arange(len(prices)), index=prices.index, columns=['val'])

    shares = {}
    for name in names:
        shares[name] = 0
        
    order_idx = 0
    for i in range(len(portvals)):
        while order_idx < len(order_df.index) and portvals.index[i] == order_df.index[order_idx]:
            sign = 1 if order_df['Order'].iloc[order_idx] == 'BUY' else -1
            num = order_df['Shares'].iloc[order_idx]
            sym = order_df['Symbol'].iloc[order_idx]
            shares[sym] += sign * num
            cash -= (sign + impact) * num * prices[sym].iloc[i]
            cash -= commission
            order_idx += 1
        portvals.iloc[i] = cash
        for key in shares:
            portvals.iloc[i] += shares[key] * prices[key].iloc[i]
    print portvals[:20]
    return portvals

def author():
    return 'schou33'

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/order_short.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    # start_date = dt.datetime(2008,1,1)
    # end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    start_date = portvals.index[0]
    end_date = portvals.index[-1]

    dates = pd.date_range(start_date, end_date)
    prices_all = get_data(['GOOG'], dates)
    prices_SPY = prices_all['SPY']
    cum_ret = (portvals[-1] / portvals[0]) - 1
    daily_returns =  (portvals / portvals.shift(1)) - 1
    daily_returns = daily_returns[1:]
    avg_daily_ret = daily_returns.mean()
    std_daily_ret = daily_returns.std()
    sharpe_ratio = math.sqrt(252) * (avg_daily_ret - 0) / std_daily_ret


    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
