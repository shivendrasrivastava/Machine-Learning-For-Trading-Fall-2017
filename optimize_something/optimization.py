"""MC1-P2: Optimize a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import scipy.optimize as spo
from util import get_data, plot_data


def f(X, normed):
    alloced = normed * X
    port_val = alloced.sum(axis=1)

    daily_returns =  (port_val[1:] / port_val[:-1]) - 1

    Y = daily_returns.std()

    return Y

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    prices_SPY /= prices_SPY[0]


    prices.fillna(method='ffill', inplace=True)
    prices.fillna(method='bfill', inplace=True)
    normed = prices / prices.ix[0]


    only_prices = normed.values
    ### Sharpe Ratio = 252**0.5 * adr / sddr;

    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    # allocs = np.asarray([1 for x in range(len(syms))]) # add code here to find the allocations
    allocs = np.ones(len(syms))
    allocs /= allocs.sum()
    Xguess = allocs
    cons = ({'type': 'eq', 'fun': lambda x: sum(x) - 1})
    bnds = [(0, 1) for x in range(len(syms))]
    best_alloc = spo.minimize(f, Xguess, args = (only_prices), bounds = bnds, constraints = cons, method = 'SLSQP', options = {'ftol': 1e-8})

    # Get daily portfolio value

    allocs = best_alloc.x
    alloced = normed * allocs
    port_val = alloced.sum(axis=1)
    daily_returns = (port_val / port_val.shift(1)) - 1
    daily_returns = daily_returns[1:]
    cr = port_val[-1] - 1 #### wait a min
    adr = daily_returns.mean()
    sddr = daily_returns.std()

    sr = 252**0.5 * adr / sddr

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp)
        pass

    return allocs, cr, adr, sddr, sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2008,6,1)
    end_date = dt.datetime(2009,6,1)
    symbols = ['IBM', 'X', 'GLD']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
