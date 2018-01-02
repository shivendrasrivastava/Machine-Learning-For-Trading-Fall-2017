# An improved version of your marketsim code that accepts a "trades" data frame
# (instead of a file). More info on the trades data frame below.
import pandas as pd
import numpy as np
import math
import datetime as dt
import types
import os
from util import get_data, plot_data

def marketsim(df_trades, prices, sv=100000, sh = 0, commission = 0, impact = 0):
    df_holding = pd.DataFrame(data=np.ones(len(prices)) * sh, index=prices.index, columns=['val'])
    df_cash = pd.DataFrame(data=np.ones(len(prices)) * sv, index=prices.index, columns=['val'])
    for i in range(len(prices.index)):
        cash_change = 0
        sign = 1 if df_trades.values[i][0] > 0 else -1

        if df_trades.values[i][0] != 0:
            cash_change = (sign + impact) * abs(df_trades.values[i][0]) * prices.values[i][0]
            cash_change += commission
        if i == 0:
            df_cash['val'].iloc[i] -= cash_change
            df_holding['val'].iloc[i] += df_trades.values[i][0]
            continue
        df_cash['val'].iloc[i] = df_cash['val'].iloc[i - 1] - cash_change
        df_holding['val'].iloc[i] = df_holding['val'].iloc[i - 1] + df_trades.values[i][0]
    # print df_holding
    df_share_val = pd.np.multiply(df_holding, prices)
    portvals = df_share_val + df_cash
    return portvals

if __name__ == "__main__":
    names = ['JPM']
    start_date = '2008-01-01'
    end_date = '2009-12-31'
    prices = get_data(names, pd.date_range(start_date, end_date))
    # print len(prices.index)
    prices = prices[names]
    # v1 = prices.reindex(columns=names).values
    # print v1
    df_trades = pd.DataFrame(data=np.random.randint(-1, 2, size=len(prices.index))*1000, index=prices.index, columns = ['val'])
    portvals = marketsim(df_trades, prices)
    print portvals
