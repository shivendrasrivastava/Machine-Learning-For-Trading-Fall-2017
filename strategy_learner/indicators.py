'''
ShuHo Chou: schou33
'''
# Your code that implements your indicators as functions that operate on dataframes.
# The "main" code in indicators.py should generate the charts that illustrate your indicators in the report.
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import datetime as dt
import types
import os
from util import get_data, plot_data

def author():
    return 'schou33'

def moving_average(vals, window = 10):
    ret = np.cumsum(vals, dtype = float)
    ret[window :] = ret[window :] - ret[: -window]
    return ret[window - 1 : -1] / window

def exp_moving_average(vals, N = 12):
    alpha = 2 / float(N + 1)
    EMA = [0] * len(vals)
    EMA[0] = vals[0]
    for i in range(1, len(vals)):
        EMA[i] = EMA[i - 1] * (1 - alpha) + vals[i] * alpha
    return np.array(EMA)

def simple_moving_average(prices, window = 10, show_pic = True):
    prices = prices / prices.ix[0]
    price_val = np.array(prices.values)
    moving_avg = np.concatenate((np.array([np.nan] * (window)), moving_average(price_val, window = window)))
    df_moving_avg = pd.DataFrame(data=moving_avg, index=prices.index, columns=['val'])
    ind = price_val / moving_avg - 1
    if show_pic:
        pr, = plt.plot(prices, 'g')
        ma, = plt.plot(df_moving_avg, 'r')
        plt.legend([ma, pr], ['Moving Average', 'Price'])
        plt.show()
    return ind

def bollinger_band(prices, window = 10, show_pic = True):
    ind = [0] * len(prices.index)
    prices = prices / prices.ix[0]
    price_val = np.array(prices.values)
    moving_avg = np.concatenate((np.array([np.nan] * (window)), moving_average(price_val, window = window)))
    moving_std = np.array([np.nan] * window + [price_val[start : start + window].std() for start in range(len(ind) - window)])

    df_moving_avg = pd.DataFrame(data=moving_avg, index=prices.index, columns=['val'])
    df_moving_std = pd.DataFrame(data=moving_std, index=prices.index, columns=['val'])



    BB = (price_val - moving_avg) / (moving_std * 2)
    if show_pic:
        pr, = plt.plot(prices, 'g')
        ma, = plt.plot(df_moving_avg, 'r')
        up, = plt.plot(df_moving_avg + 2 * df_moving_std, 'b')
        down, = plt.plot(df_moving_avg - 2 * df_moving_std, 'b')
        plt.legend([ma, pr, up], ['Moving Average', 'Price', 'Bollinger Band'])
        plt.show()
    return BB

def exponential_moving_average(prices, window = 10, show_pic = True):
    prices = prices / prices.ix[0]
    price_val = np.array(prices.values)
    EMA = exp_moving_average(price_val, N = window)
    df_EMA = pd.DataFrame(data=EMA, index=prices.index, columns=['val'])
    ind = price_val / EMA - 1
    if show_pic:
        pr, = plt.plot(prices, 'g')
        ma, = plt.plot(df_EMA, 'r')
        plt.legend([ma, pr], ['Moving Average', 'Price'])
        plt.show()
    return ind



if __name__ == '__main__':
    names = 'JPM'
    start_date = '2008-01-01'
    end_date = '2009-12-31'
    prices = get_data([names], pd.date_range(start_date, end_date))
    prices = prices[names]
    exponential_moving_average(prices)
