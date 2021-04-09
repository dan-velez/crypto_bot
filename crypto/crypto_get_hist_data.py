#!/usr/bin/python3
# crypto_get_hist_data.py - Use CCXT lib to retrieve data on 
# tickers.
# TODO:
#   get_hist_all (vexchange, vtickers, vtimeframe='1m')
#   run functions
#   find tickers with greatest change % since day start

import json
import datetime
import time
import math

import pandas as pd
import ccxt


# DATA FEED FROM EXCHANGE
exchange = str('binance')
symbol = str('ARK/ETH')
timeframe = str('1m')
exchange_out = str(exchange)
start_date = str('2021-04-09 00:00:00')
get_data = True


def to_unix_time(timestamp):
    # start of epoch time
    epoch = datetime.datetime.utcfromtimestamp(0)  
    # plugin your time object
    my_time = datetime.datetime.strptime(timestamp, 
            "%Y-%m-%d %H:%M:%S")
    delta = my_time - epoch
    return delta.total_seconds() * 1000


# File Name
symbol_out = symbol.replace("/", "")
filename = './historical/{}-{}-{}.json'.format(
        exchange_out, symbol_out, timeframe)

# Get our Exchange
exchange = getattr(ccxt, exchange)()
exchange.load_markets()
hist_start_date = int(to_unix_time(start_date))

data = exchange.fetch_ohlcv(symbol, 
        timeframe, since=hist_start_date)
if len(data) == 0:
    print("[* crypto_get_hist_data] No data found for %s" 
            % symbol)
    import sys
    sys.exit()

vres = {
    "initial": data[0][1],
    "history": []
}

# Parse to JSON
for vbar in data:
    vres['history'].append({
        'timestamp': str(pd.to_datetime(vbar[0], unit='ms')),
        'open': vbar[1],
        'high': vbar[2],
        'low': vbar[3],
        'close': vbar[4],
        'volume': vbar[5],
        'symbol': symbol
    })

print(len(data))
print(json.dumps(vres, indent=4))
open(filename, 'w+').write(json.dumps(vres, indent=4))

# Parse as CSV
# header = [
# 'Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
# df = pd.DataFrame(data, columns=header)
# df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
# df['Timestamp'] = df['Timestamp'].dt.strftime('%Y%m%d %H%M')
# df[['Volume']] = df[['Volume']].astype(int)
# df.to_csv(filename, index= False,header=False, sep=';')
