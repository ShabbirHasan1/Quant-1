# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 17:53:26 2021

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

# Drawdown

def max_drawdown(dframe):
    df = dframe.copy()
    df['return'] = df['Adj Close'].pct_change(1)
    df['cum_return'] = (1 + df['return']).cumprod()
    df['cum_rolling_max'] = df['cum_return'].cummax()
    df['drawdown'] = df['cum_rolling_max'] - df['cum_return']
    return (df['drawdown']/df['cum_rolling_max']).max()

# Calamar Ratio

def calamar(dframe):
    df = dframe.copy()
    return CAGR(df)/max_drawdown(df)


# Loop
for x in tickers:
    print(f'Max drawdown for {x} is {round(max_drawdown(ohlcv_data[x]),4)}')
    print(f'Calamar Ratio for {x} is {round(calamar(ohlcv_data[x]),4)}')
    print('\n')


