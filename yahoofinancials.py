# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 17:01:49 2021

@author: User
"""

from yahoofinancials import YahooFinancials

ticker = 'SBIN.NS'
yahoo_financials = YahooFinancials(ticker)
data = yahoo_financials.get_historical_price_data('2020-01-01','2021-01-01',time_interval = 'daily')

# We can't get intraday data using this

data[ticker]['prices'][2]

import pandas as pd

df = pd.DataFrame(data = {'col1':[1,2],'col2':[5,6]})

df = pd.DataFrame(data = data[ticker]['prices'])
df.drop(columns = 'date', inplace = True)
df['formatted_date'] = pd.to_datetime(df['formatted_date'])
df.set_index('formatted_date', inplace = True)

# Loading Data with yahoofinancials API
import datetime as dt

json_data = YahooFinancials('GOOG').get_historical_price_data((dt.date.today()-dt.timedelta(365)).strftime('%Y-%m-%d'), dt.date.today().strftime('%Y-%m-%d'),time_interval = 'daily')

# --------------------------------------------------------------------

def pd_yahoo_financials(ticker, start, end, interval):
    
    json_data = YahooFinancials(ticker).get_historical_price_data(start, end, time_interval = interval)
    df = pd.DataFrame(data = json_data[ticker]['prices'])
    df.drop(columns = 'date', inplace = True)
    df['date'] = pd.to_datetime(df['formatted_date'])
    df.drop(columns = 'formatted_date', inplace = True)
    df.set_index('date', inplace = True)
    df.dropna(inplace = True)
    
    return df

# ---------------------------------------------------------------------

amzn = pd_yahoo_financials('AMZN', '2020-01-11', dt.date.today().strftime('%Y-%m-%d'), 'daily')

# For multiple stocks

stocks = ['AMZN', 'AAPL', 'GOOG', 'MSFT']
stock_data = {}

for x in stocks:
    stock_data[x] = pd_yahoo_financials(x, '2015-01-01', dt.date.today().strftime('%Y-%m-%d'), 'daily')

# ----------------------------------------------------------------------

# Using alpha_vantage 

key_path = 'E:\\Online Courses\Algo Trading\\api_alpha_vantage.txt'

from alpha_vantage.timeseries import TimeSeries

# Data from a single ticker

ts = TimeSeries(key = open(key_path, 'r').read(), output_format='pandas')
data = ts.get_daily(symbol = 'BTCUSD', outputsize='full')[0]
data.colum = ['open', 'high', 'low', 'close', 'volume']
data.iloc[::-1]

# Data from multiple stocks

import time

stocks = ['AMZN', 'GOOG', 'AAPL', 'FB', 'TSLA', 'CSCO', 'MSFT']
close_prices = pd.DataFrame()
api_call_count = 0
for x in stocks:
    starttime = time.time()
    ts = TimeSeries(key = open(key_path, 'r').read(), output_format='pandas')
    data = ts.get_intraday(symbol = x, outputsize='compact', interval = '1min')[0]
    api_call_count += 1
    data.columns = ['open', 'high', 'low', 'close', 'volume']
    data.iloc[::-1]
    close_prices[x] = data['close']
    if api_call_count == 5:
        api_call_count = 0
        time.sleep(60 - (time.time() - starttime))
