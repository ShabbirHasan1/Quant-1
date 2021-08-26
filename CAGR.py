# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 19:42:36 2021

@author: User
"""

# CAGR

import pandas as pd
import numpy as np
import yfinance as yf

tickers = ['SBIN.NS', 'TATAMOTORS.NS', 'WIPRO.NS']
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

for x in tickers:
    print(f'CAGR for {x} is {100*CAGR(ohlcv_data[x])}%\n') 