# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 22:58:32 2021

@author: User
"""

import pandas as pd
import numpy as np
import pandas_datareader as web
import yfinance as yf
import matplotlib.pyplot as plt
%matplotlib inline

yf.pdr_override()

start = pd.to_datetime('2011-01-01')
end = pd.to_datetime('2018-12-31')

tatamotors = web.data.get_data_yahoo('TATAMOTORS.NS', start = start, end = end)
tcs = web.data.get_data_yahoo('TCS.NS', start = start, end = end)
wipro = web.data.get_data_yahoo('WIPRO.NS', start = start, end = end)
ibrealest = web.data.get_data_yahoo('IBREALEST.NS', start = start, end = end)
ongc = web.data.get_data_yahoo('ONGC.NS', start = start, end = end)

tatamotors = tatamotors[['Adj Close']]
tcs = tcs[['Adj Close']]
wipro = wipro[['Adj Close']]
ibrealest = ibrealest[['Adj Close']]
ongc = ongc[['Adj Close']]

stocks = pd.concat([tatamotors, tcs, wipro, ibrealest, ongc], axis = 1)
stocks.columns = ['tatamotors', 'tcs', 'wipro', 'ibrealest', 'ongc']

log_ret = np.log(stocks/stocks.shift(1))

def get_ret_vol_sr(weights):
    weights = np.array(weights)
    ret = np.sum(log_ret.mean() * weights)*252
    vol = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov()*252, weights)))
    sr = ret/vol
    return np.array([ret, vol, sr])

from scipy.optimize import minimize

def neg_sharpe(weights):
    return get_ret_vol_sr(weights)[2]*(-1)

def check_sum(weights):
    # return 0 if the sum of weights is 1
    # else it returns how off you are from 1
    return np.sum(weights) - 1

cons = ({'type':'eq', 'fun':check_sum})
bounds = ((0,1),(0,1),(0,1),(0,1),(0,1))
init_guess = [0.2,0.2,0.2,0.2,0.2]
# opt_results = minimize(neg_sharpe, init_guess, method='SLSQP', bounds=bounds, constraints=cons)
# get_ret_vol_sr(opt_results.x)
frontier_y = np.linspace(0,0.3,100)


def minimize_vol(weights):
    return get_ret_vol_sr(weights)[1]

frontier_volatility = []

for possible_return in frontier_y:
    cons = ({'type':'eq', 'fun':check_sum},
            {'type':'eq', 'fun': lambda w: get_ret_vol_sr(w)[0] - possible_return})
    
    result = minimize(minimize_vol, init_guess, method='SLSQP', bounds=bounds, constraints= cons)
    
    frontier_volatility.append(result['fun'])

plt.plot(frontier_volatility, frontier_y, 'g--', lw = 3)

# For Sharpe Ratio:
    
# get_ret_vol_sr(opt_results.x)