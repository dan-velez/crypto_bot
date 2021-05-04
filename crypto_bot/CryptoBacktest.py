#!/usr/bin/python

import json

from termcolor import colored

from crypto_broker import is_open


class CryptoBacktest:
    """Backtest on historical data using history file and a strategy class."""

    def run (self, broker, strategy, vhist):
        # Loop through bars
        # Test open / exit conditions on each
        print("[* Backtest] Period Start Price: %s\n" % vhist['initial'])

        for vbar in vhist['history']:
            vsymb = vbar['symbol']
            print("[* Backtest] %s @ %s" % (vsymb, vbar['close']))

            if broker.is_open(vsymb):
                # SELL?
                if strategy.should_close(): 
                    broker.sell(vsymb, strategy.vtrade_quantity)
            else:
                # BUY?
                if strategy.should_open(vbar, vhist):
                    broker.buy(vsymb, strategy.vtrade_quantity)
        
        print(port_total())


if __name__ == "__main__":
    # Test class funcionality.
    import sys

    if len(sys.argv) < 2:
        print("[*] Usage: crypto_backtest.py <symbol_history_file.json>")
        sys.exit()

    # Load history file
    vhist_file = sys.argv[1]
    vjson_hist = json.loads(open(vhist_file, 'r').read())
    print("[* Backtest] %s bars available." %len(vjson_hist['history']))

    # Run backtest with open / close signals.
    from CryptoStrategy import CryptoStrategy
    strat = CryptoStrategy()
    tester = CryptoBacktest()
    tester.run(strat, vjson_hist)