# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 17:07:34 2021

@author: User
"""
#
# TECHNICAL INDICATORS
#

import pandas as pd
import yfinance as yf
import numpy as np
import stocktrends as st

# Downloading historical data of following stocks
stocks = ['TCS.NS', 'INFY.NS', 'WIPRO.NS']
ohlcv_data = {}
hour_data = {}

# Looping over tickers
for x in stocks:
    temp = yf.download(x, period = '1mo', interval = '5m')
    temp.dropna(how = 'any', inplace = True)
    ohlcv_data[x] = temp

for x in stocks:
    temp = yf.download(x, period = '1y', interval = '1h')
    temp.dropna(how = 'any', inplace = True)
    hour_data[x] = temp


# MACD Function

def MACD(dframe, a=12, b=26, c=9):
    #  a,b,c are Windows for fast, slow MAs and signal line
    df = dframe.copy()
    df['ma_fast'] = df['Adj Close'].ewm(span = a, min_periods = a).mean()
    df['ma_slow'] = df['Adj Close'].ewm(span = b, min_periods = b).mean()
    df['macd'] = df['ma_fast'] - df['ma_slow']
    df['signal'] = df['macd'].ewm(span = c, min_periods = c).mean()
    return df.loc[:,['macd', 'signal']]

# Looping MACD for all tickers
for x in stocks:
    ohlcv_data[x][['MACD','Signal']] = MACD(ohlcv_data[x])
    
# ATR Function 

def ATR(dframe, n=14):
    df = dframe.copy()
    df['H-L'] = df['High'] - df['Low']
    df['H-PrevClose'] = df['High'] - df['Adj Close'].shift(1)
    df['L-PrevClose'] = df['Low'] - df['Adj Close'].shift(1)
    df['True_Range'] = df[['H-L', 'H-PrevClose', 'L-PrevClose']].max(axis=1, skipna = False)
    df['ATR'] = df['True_Range'].ewm(com = n, min_periods = n).mean()
    return df['ATR']

# Looping ATR for all tickers
for x in stocks:
    ohlcv_data[x]['ATR'] = ATR(ohlcv_data[x])
    
# Bollinger Bands Function

def BolBands(dframe,ma_window=20, std_multiplier=2):
    df = dframe.copy()
    df['Middle_Band'] = df['Adj Close'].rolling(ma_window).mean()
    df['Upper_BB'] = df['Middle_Band'] + (std_multiplier*df['Adj Close'].rolling(ma_window).std(ddof=0))
    df['Lower_BB'] = df['Middle_Band'] - (std_multiplier*df['Adj Close'].rolling(ma_window).std(ddof=0))
    df['BB_width'] = df['Upper_BB'] - df['Lower_BB']
    return df[['Middle_Band', 'Upper_BB', 'Lower_BB', 'BB_width']]

# Looping BB for all tickers
for x in stocks:
    ohlcv_data[x][['Middle_Band', 'Upper_BB', 'Lower_BB', 'BB_width']] = BolBands(ohlcv_data[x])

# Relative Strength Indicator (RSI) Function

def RSI(dframe, window=14):
    df = dframe.copy()
    df['change'] = df['Adj Close'] - df['Adj Close'].shift(1)
    df['Gain'] = np.where(df['change']>=0, df['change'], 0)
    df['Loss'] = np.where(df['change']<0, -1*df['change'], 0)
    df['avgGain'] = df['Gain'].ewm(alpha = 1/window, min_periods = window).mean()
    df['avgLoss'] = df['Loss'].ewm(alpha = 1/window, min_periods = window).mean()
    df['RS'] = df['avgGain']/df['avgLoss']
    df['RSI'] = 100 - (100/(1+df['RS']))
    return df['RSI']

# Looping RSI for all tickers
for x in stocks:
    ohlcv_data[x]['RSI'] = RSI(ohlcv_data[x])
    
# Average Directional Index (ADX) Function

def ADX(dframe, window=14):
    df = dframe.copy()
    df['ATR'] = ATR(df, window)
    # DM is Directional Movement
    # Comparing High & Highs, and Low & Lows 
    df['upmove'] = df['High']-df['High'].shift(1)
    df['downmove'] = df['Low'].shift(1)-df['Low']                      
    df['DM+'] = np.where((df['upmove'] > df['downmove']) & df['upmove'] > 0,df['upmove'],0)
    df['DM-'] = np.where((df['downmove'] > df['upmove']) & df['downmove'] > 0 ,df['downmove'],0)

    # DI is Directional Indicator
    df['DI+'] = (100*df['DM+']/df['ATR']).ewm(com=window,min_periods=window).mean()
    df['DI-'] = (100*df['DM-']/df['ATR']).ewm(com=window,min_periods=window).mean()
    df['DI_sum'] = abs(df['DI+'] + df['DI-'])
    df['DI_diff'] = abs(df['DI+'] - df['DI-'])
    df['DX'] = 100*df['DI_diff']/df['DI_sum']
    df['ADX'] = df['DX'].ewm(com=window, min_periods=window).mean()
    return df['ADX']

# Looping ADX for all tickers
for x in stocks:
    ohlcv_data[x]['ADX'] = ADX(ohlcv_data[x])


# Renko Function

renko_data ={}

def renko_df(dframe, hourly_df):
    df = dframe.copy()
    df.drop('Close', axis=1, inplace = True)
    df.reset_index(inplace=True)
    df.columns = ['date','open','high','low','close','volume']
    df2 = st.Renko(df)
    df2.brick_size = round(ATR(hourly_df,120).iloc[-1],0)*3
    return df2.get_ohlc_data()

# Looping Renko for all tickers
for x in stocks:
    renko_data[x] = renko_df(ohlcv_data[x], hour_data[x])
