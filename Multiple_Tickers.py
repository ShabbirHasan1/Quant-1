# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 14:54:53 2021

@author: User
"""

import yfinance as yf

data = yf.download('SBIN.NS', start = '2020-08-13', end = '2021-08-20', interval = '1wk')

# Trying for multiple stocks

import datetime as dt
import pandas as pd

stocks = ['AMZN', 'AAPL', 'TATAMOTORS.NS', 'WIPRO.NS', '3988.HK']
start = dt.datetime.today()-dt.timedelta(30)
end = dt.datetime.today()
cl_price = pd.DataFrame() # empty dataframe which will be filled with closing prices of each stock
ohlcv_data = {} # empty dictionary which will be filled with ohlcv dataframe for each ticker

# looping over tickers and creating a dataframe with close prices
for ticker in stocks:
    cl_price[ticker] = yf.download(ticker,start,end)["Adj Close"]

# looping over tickers and storing OHLCV dataframe in dictionary
for ticker in stocks:
    ohlcv_data[ticker] = yf.download(ticker,start,end)

