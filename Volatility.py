# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 16:49:14 2021

@author: User
"""

# Volatility

import pandas as pd
import numpy as np
import yfinance as yf

tickers = ['HCLTECH.NS', 'TCS.NS', 'WIPRO.NS', 'INFY.NS']
ohlcv_data = {}

for x in tickers:
    temp = yf.download(x,period='7mo',interval='1d')
    temp.dropna(how='any',inplace=True)
    ohlcv_data[x] = temp

def volatility(dframe):
    df = dframe.copy()
    return df['Adj Close'].pct_change(1).std()*np.sqrt(252)

for x in tickers:
    print(f'Annualised Volatility of {x} = {round(100*volatility(ohlcv_data[x]),2)}%')
    
