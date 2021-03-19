# sma_cross_2 - Strategy using SMA.

import backtrader as bt


class SmaCross2 (bt.Strategy):

    def __init__ (self):  # Initiation
        self.sma = bt.ind.SimpleMovingAverage(period=15)  # Processing

    def next (self):  # Processing
        for i in range(0,len(self.datas)):
            print(f'{self.datas[i].datetime.datetime(ago=0)} \
    {self.datas[i].p.dataname}: \
    o:{self.datas[i].open[0]} \
    h:{self.datas[i].high[0]} \
    l:{self.datas[i].low[0]} \
    c:{self.datas[i].close[0]} \
    v:{self.datas[i].volume[0]}' )

        if self.sma > self.data.close:
            # Do something
            pass

        elif self.sma < self.data.close: # Post-processing
            # Do something else
            pass