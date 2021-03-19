# strat_test.py - Test strategy from Backtrader tutorials.

import backtrader as bt


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