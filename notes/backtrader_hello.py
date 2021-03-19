# Backtrader examples and tutorials.
#
# Data feeds have lines. Lines are connections of points.
# A data feed has following points: Open, High, Low, Close, Volume, OpenInterest.
# A series of "Opens" along a time is a line.
# A Data Feed usually has *6* lines. (for each series of points).
# If we count DateTime, which is the index, there are 7 lines.
#
# Purpose of strategy is to multiply cash by operating on the DataFeed.
# 3 main components: Data Feed, Cash Amount, and Strategy


import backtrader as bt

import datetime
import sys
import os


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # Get the path of historical data. 
    datapath = os.path.abspath(sys.argv[0])

    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(2020, 11, 1),
        # Do not pass values after this date
        todate=datetime.datetime(2021, 2, 10),
        reverse=False)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    cerebro.broker.setcash(100)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Runs a line of data. Or DataFeed.
    # At each point the strategy is ran?
    # In no broker specified, start with default broker.
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())