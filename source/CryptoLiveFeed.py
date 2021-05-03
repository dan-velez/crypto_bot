#!/usr/bin/python
import time

from termcolor import colored
import ccxt


class CryptoLiveFeed:
    """Run a CryptoStrategy on a list of assets"""
    
    def __init__ (self, assets=[], strategy=None, broker=None):
        self.assets = assets
        self.strategy = strategy
        self.broker = broker

    def run (self, vinterval=5):
        """Run loop on all assets and run strategy on each asset."""

        # Initiate exchanges first.
        vexchanges = {}
        for vex in self.assets:
            vexchanges[vex['name']] = getattr(ccxt, vex['name'])()

        # Loop through coins within exchanges.
        while True:
            for vex in self.assets:
                for vcoin in vex['coins']:
                    print(vcoin['symbol'])

                    # Run strategy here.
                    if broker.is_open(vsymb):
                        # SELL?
                        if strategy.should_close(): 
                            broker.sell(vsymb, strategy.vtrade_quantity)
                    else:
                        # BUY?
                        if strategy.should_open(vbar, vhist):
                            broker.buy(vsymb, strategy.vtrade_quantity)

            # Print message after each succesful iteration on target assets.
            print("[* LiveFeed] Finished iteration. Waiting...")
            time.sleep(vinterval)


if __name__ == "__main__":
    # Test class functions
    import json
    from CryptoBroker import CryptoBroker
    
    assets =  json.loads(open('data\\coins_coinbasepro.json', 'r').read())
    broker = CryptoBroker()

    live_feed = CryptoLiveFeed(assets=assets, strategy=None, broker=broker)
    live_feed.run()