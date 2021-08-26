# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 17:25:43 2021

@author: User
"""

import pandas as pd
import numpy as np
import yfinance as yf

tickers = ['HCLTECH.NS', 'TCS.NS', 'WIPRO.NS', 'INFY.NS']
ohlcv_data = {}

for x in tickers:
    temp = yf.download(x,period='7mo',interval='1d')
    temp.dropna(how='any',inplace=True)
    ohlcv_data[x] = temp
    
def CAGR(dframe):
    df = dframe.copy()
    df['return'] = df['Adj Close'].pct_change(1)
    df['cum_return'] = (1 + df['return']).cumprod()
    n = len(df)/252
    return round(((df['cum_return'][-1])**(1/n)) - 1,4)

def volatility(dframe):
    df = dframe.copy()
    return df['Adj Close'].pct_change(1).std()*np.sqrt(252)

# Sharpe Ratio

def sharpe(dframe, rf=0.03):
    # rf = risk free rate
    df = dframe.copy()
    return (CAGR(df) - rf)/volatility(df)
    
# Sortino Ratio

def Sortino(dframe, rf=0.03):
    df = dframe.copy()
    df['return'] = df['Adj Close'].pct_change(1)
    neg_ret = np.where(df['return']>0, 0, df['return'])
    neg_vol = pd.Series(neg_ret[neg_ret!=0]).std()*np.sqrt(252)
    return (CAGR(df) - rf)/neg_vol

# Looping

for x in tickers:
    print(f'Sharpe Ratio for stock {x} is {round(sharpe(ohlcv_data[x]),2)}')
    print(f'Sortino Ratio for stock {x} is {round(Sortino(ohlcv_data[x]),2)}')
    print('\n')
    