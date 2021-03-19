# How to use Alpaca DataFeed
 
import alpaca_backtrader_api
import backtrader as bt

from datetime import datetime
from datetime import time

ALPACA_API_KEY = "PK3ORH49BYXSS87641CJ"
ALPACA_SECRET_KEY = "XMGkMQtY7F76Qf8qRehVNzjvDWFgSjGVmNK3jwCO"
ALPACA_PAPER = True


# Demo Strategy
class TestStrategy (bt.Strategy):
    
    def log (self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__ (self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def next (self):
        # Simply log the closing price of the series from the reference
        # self is the point of the ticker in a line.
        self.log('Close, %.2f' % self.dataclose[0])

        # If the position has fallen 3 sessions in a row, BUY.
        if self.dataclose[0] < self.dataclose[-1]:
            # current close less than previous close

            if self.dataclose[-1] < self.dataclose[-2]:
                # previous close less than the previous close
                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.buy()


if __name__ == "__main__":
    # Example get DataFeed from Alpaca.)

    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    cerebro.broker.setcash(100)
    
    store = alpaca_backtrader_api.AlpacaStore(
        key_id=ALPACA_API_KEY,
        secret_key=ALPACA_SECRET_KEY,
        paper=ALPACA_PAPER
    )

    # Get intraday data from one day of penny stock.
    # Try for all different stocks everyday.
    DataFactory = store.getdata

    # read file, for each stock, add to datafeed. Use yesterdays date.
    data0 = DataFactory(
        dataname='GEN',
        timeframe=bt.TimeFrame.Minutes,
        historical=True, 
        
        fromdate=datetime(2021, 3, 1),
        todate=datetime(2021, 3, 11),
        # sessionstart=time(9, 0),
        # sessionend=time(16, 0),

        dtformat= '%Y-%m-%dT%H:%M:%S%z',
        compression=1)

    cerebro.adddata(data0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

# for ticker in tickers:
#     for timeframe, minutes in timeframes.items():
#         print(f'Adding ticker {ticker} using {timeframe} timeframe at {minutes} minutes.')

#         d = DataFactory(
#             dataname=ticker,
#             timeframe=bt.TimeFrame.Minutes,
#             compression=minutes,
#             fromdate=fromdate,
#             todate=todate,
#             historical=True)

#         cerebro.adddata(d)