# alpaca_api_test.py - Test alpaca functions.

import alpaca_trade_api as tradeapi
import json
from datetime import datetime
import pandas as pd
import sys

# Paper
api_key = 'PK3ORH49BYXSS87641CJ' 
api_secret = 'XMGkMQtY7F76Qf8qRehVNzjvDWFgSjGVmNK3jwCO'
base_url = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v1')
# vapi = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')


# Get minute price data.
NY = 'America/New_York'
barset = api.get_barset(
    'NAKD', 
    '1Min', 
    limit=480,
    start=pd.Timestamp('2021-03-10', tz=NY).isoformat(),
    end=pd.Timestamp('2021-03-11', tz=NY).isoformat())

# print(barset._raw)
# vjson = json.loads(str(barset))
print(barset.df)
barset.df.to_csv('historical\\NAKD_0310.csv')
# print(json.dumps(barset._raw, indent=4))

sys.exit()


# Print out timestamps
for vbar in barset._raw['GEN']:
    # print(vbar['t'])
    pass

aapl_bars = barset['GEN']
# See how much AAPL moved in that timeframe.
week_open = aapl_bars[0].o
week_close = aapl_bars[-1].c
percent_change = (week_close - week_open) / week_open * 100
print('GEN moved {} %'.format(percent_change))