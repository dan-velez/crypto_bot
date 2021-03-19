# strat_runner.py - Runs a strategy on a datafeed.
# Use ticker.json to load symbols, then run on intraday timeframe. 

import alpaca_backtrader_api as alpaca
import backtrader as bt
import backtrader.feeds as btfeeds

from datetime import datetime
from datetime import time

# Strategies
from strategies.strat_rsi_stack import RSIStack
from strategies.strat_sma_cross_2 import SmaCross2
from strategies.strat_sma_cross_1 import SmaCross
from strategies.strat_test import TestStrategy
from strategies.strat_donchian_channels import DCChannels

# Init broker API.
ALPACA_KEY_ID = 'PK3ORH49BYXSS87641CJ'
ALPACA_SECRET_KEY = 'XMGkMQtY7F76Qf8qRehVNzjvDWFgSjGVmNK3jwCO'
ALPACA_PAPER = True

# Init cerebro.
cerebro = bt.Cerebro()

# cerebro.addstrategy(RSIStack)
# cerebro.addstrategy(SmaCross)
cerebro.addstrategy(SmaCross2)
# cerebro.addstrategy(TestStrategy)
# cerebro.addstrategy(DCChannels)

cerebro.broker.setcash(100)
cerebro.broker.setcommission(commission=0.0)


## Set DataFeed Generic CSV ####################################################

vdata = btfeeds.GenericCSVData(
    dataname="historical\\NAKD_0310.csv",
    datetime=0,
    time=-1,
    open=1, high=2, low=3, close=4, volume=5, openinterest=-1,
    dtformat="%Y-%m-%d %H:%M:%S-05:00",
    # 2021-03-10 09:30:00-05:00
    
    timeframe=bt.TimeFrame.Minutes,
    compression=1,

    fromdate=datetime(2021, 3, 10, 9, 30),
    todate=datetime(2021, 3, 10, 17, 0),

    sessionstart=time(9, 30),
    sessionend=time(17, 0)
)
cerebro.adddata(vdata)


## Set DataFeed Alpaca Live ####################################################

if False:
    # Init DataFeed. Add one DataFactory per symbol.
    store = alpaca.AlpacaStore(
        key_id=ALPACA_KEY_ID,
        secret_key=ALPACA_SECRET_KEY,
        paper=ALPACA_PAPER
    )

    if not ALPACA_PAPER:
        print(f"LIVE TRADING")
        broker = store.getbroker()
        cerebro.setbroker(broker)

    # Set DataFeed timeframes.
    # Should produce 480 records.
    fromdate = datetime(2021, 3, 10, 9, 0)
    todate = datetime(2021, 3, 10, 17, 0)

    # tickers = ['GEN', 'TRX', 'ACST']
    tickers = ['GOOG']

    DataFactory = store.getdata

    for ticker in tickers:
        d = DataFactory(
            dataname=ticker,
            timeframe=bt.TimeFrame.Minutes,
            compression=1,
            
            fromdate=fromdate,
            todate=todate,
            sessionstart=time(9, 0),
            sessionend=time(17, 30),

            historical=True)

        cerebro.adddata(d)

################################################################################

# Run strategy.
cerebro.run()
print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
# cerebro.plot(style='candlestick', barup='green', bardown='red')