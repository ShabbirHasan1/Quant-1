# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 12:31:16 2021

@author: User
"""

import datetime as dt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

stocks = ['FB', 'AMZN', 'GOOG', 'CSCO'] #, 'MSFT', 'AAPL', 'T', 'BA', 'C', 'WMT', 'DIS']
start = dt.datetime.today()-dt.timedelta(3650)
end = dt.datetime.today()
cl_price = pd.DataFrame() # empty dataframe which will be filled with closing prices of each stock
# ohlcv_data = {} # empty dictionary which will be filled with ohlcv dataframe for each ticker
cl_price = cl_price[::-1]
# looping over tickers and creating a dataframe with close prices
for ticker in stocks:
    cl_price[ticker] = yf.download(ticker,start,end)["Adj Close"]
# cl_price.isnull().values.any()

# cl.print.fillna()   

cl_price.dropna(axis = 1, how = 'any', inplace = True) 

cl_price.mean()    
cl_price.std()
cl_price.median()
desc = cl_price.describe()
cl_price.head()
returns = cl_price.pct_change()[1:]

returns.mean()

MA10_returns= returns.rolling(window = 10, min_periods = 10).mean()

# But for financial data we use exponential MA as we give more weightage
# to the most recent data-point

ema = returns.ewm(com = 10, min_periods = 10).mean()

returns.plot() 
g = cl_price.plot(figsize = (8,6))
cl_price.plot(subplots = 1, figsize = (16,8))

returns.plot(subplots=1)

cum_returns = (1+returns).cumprod()
cum_returns.plot(figsize=(10,7),grid=1)

fig, ax = plt.subplots()
# plt.style.available
plt.style.use('dark_background')
ax.set(title = 'Mean Daily Return', xlabel = 'Stocks', ylabel = 'Mean return')
plt.bar(x = returns.columns, height = returns.mean())
# plt.bar(x = returns.columns, height = returns.std())