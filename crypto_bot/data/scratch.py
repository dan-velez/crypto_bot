#!/usr/bin/python

"""Testing code."""

import calendar
from datetime import datetime, date, timedelta
import json

import ccxt
import pandas as pd
import numpy as np


def min_ohlcv (dt, exchange, pair, limit):
    """UTC native object"""

    since = calendar.timegm(dt.utctimetuple())*1000
    ohlcv1 = exchange.fetch_ohlcv(
        symbol=pair, timeframe='1m', since=since, limit=limit)
    ohlcv2 = exchange.fetch_ohlcv(
        symbol=pair, timeframe='1m', since=since, limit=limit)
    ohlcv = ohlcv1 + ohlcv2
    return ohlcv


def ohlcv (dt, exchange, pair, period='1d'):
    """Generate OHLCV data for a 24 hour period of a day."""

    ohlcv = []
    limit = 1000
    
    if period == '1m':
        limit = 720
    elif period == '1d':
        limit = 365
    elif period == '1h':
        limit = 24
    elif period == '5m':
        limit = 288
    
    for i in dt:
        start_dt = datetime.strptime(i, "%Y%m%d")
        since = calendar.timegm(start_dt.utctimetuple())*1000
        if period == '1m':
            ohlcv.extend(min_ohlcv(start_dt, exchange, pair, limit))
        else:
            ohlcv.extend(exchange.fetch_ohlcv(
                symbol=pair, timeframe=period, since=since, limit=limit))
    
    # Convert data into readable pandas data.
    df = pd.DataFrame(ohlcv, 
        columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Time'] = [datetime.fromtimestamp(float(time)/1000) 
        for time in df['Time']]
    df['Open'] = df['Open'].astype(np.float64)
    df['High'] = df['High'].astype(np.float64)
    df['Low'] = df['Low'].astype(np.float64)
    df['Close'] = df['Close'].astype(np.float64)
    df['Volume'] = df['Volume'].astype(np.float64)
    df.set_index('Time', inplace=True)
    
    return df


def date_list (start_day="20210101", end_day="20210110"):
    """Generate array of consecutive days for a given period."""

    start_dt = datetime.strptime(start_day, "%Y%m%d")
    end_dt = datetime.strptime(end_day, "%Y%m%d")
    days_num = (end_dt - start_dt).days + 1
    datelist = [start_dt + timedelta(days=x) for x in range(days_num)]
    datelist = [date.strftime("%Y%m%d") for date in datelist]
    # df = ohlcv(datelist, 'ETH/BTC', '1h')
    # df.to_csv('data/eth_btc_1hour_2018JanTo2020Aug.csv')
    return datelist


def get_change(current, previous):
    """Caclulate change % between 2 numbers."""

    if current == previous:
        return 100.0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0


def volatility_24_hour (exchange, pair):
    """Get 24 hour change % for an asset pair in order 
    to determine volatility."""

    vdt = datetime.today().strftime("%Y%m%d")
    df = ohlcv([vdt], binance, pair, '1h')
    # print(df)
    # print(len(df))

    vres = df.to_json(orient='records')
    vres = json.loads(vres)
    # vres = json.dumps(vres, indent=4) 
    # print(vres)
    # print(vres[0]['Open'])
    # print(vres[-1]['Close'])
    return get_change(vres[-1]['Close'], vres[0]['Open'])


# Test
# binance = ccxt.binance()
# volatil = volatility_24_hour(binance, 'ETH/BTC')
# print(volatil)
# datetime.fromtimestamp(candle[0] / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')

# Testing coinbase pro API connection.
keys = json.loads(open("../.crypto.json", 'r').read())
ex = ccxt.coinbasepro({
    'apiKey': keys['cb-sandbox-apikey'],
    'secret': keys['cb-sandbox-secret'],
    'password': keys['cb-sandbox-passphrase'],
    'timeout': 30000,
    'enableRateLimit': True
})

ex.set_sandbox_mode(True)
ex.load_markets()

bal = ex.fetchBalance()
# print(json.dumps(bal, indent=4))

ex.deposit(100)

# print(json.dumps(ex.markets, indent=4))
# print(json.dumps(ex.currencies, indent=4))
