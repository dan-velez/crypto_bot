#!/usr/bin/python
import time

from termcolor import colored
import ccxt


class CryptoLiveFeed:
    """Run a CryptoStrategy on a list of assets. Loop through all the assets in
    the target asset list and run the strategy on each one."""
    
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

        # print(vexchanges['coinbasepro'].fetch_ohlcv)
        # return

        # Loop through coins within exchanges.
        while True:
            for vex in self.assets:
                for vcoin in vex['coins']:
                    print(vcoin['symbol'])

                    # Get latest price on asset.
                    vlatest_bars = vexchanges[vex['name']].fetch_ohlcv(
                        vcoin['symbol'])
                    vlatest_price = vlatest_bars[-1]
                    print(vlatest_price)

                    # Run strategy here.
                    if self.broker.is_open(vcoin['symbol']):
                        # SELL?
                        if self.strategy.should_close(): 
                            self.broker.sell(vcoin['symbol'], 
                                self.strategy.vtrade_quantity)
                    else:
                        # BUY?
                        if self.strategy.should_open({}, []):
                            self.broker.buy(vcoin['symbol'], 
                                self.strategy.vtrade_quantity)
                    
                    # Limit API request
                    print()
                    time.sleep(0.1)
                    # time.sleep(vexchanges[vex['name']].rateLimit / 1000)

            # Print message after each succesful iteration on target assets.
            print("[* LiveFeed] Finished iteration. Waiting %s sec..." 
                % vinterval)
            time.sleep(vinterval)


if __name__ == "__main__":
    # Test class functions
    import json
    from CryptoBroker import CryptoBroker
    from CryptoStrategy import CryptoStrategy # Default strategy

    assets =  json.loads(open('data\\coins_coinbasepro.json', 'r').read())
    broker = CryptoBroker()
    strategy = CryptoStrategy()

    live_feed = CryptoLiveFeed(assets=assets, strategy=strategy, broker=broker)
    live_feed.run(vinterval=3)