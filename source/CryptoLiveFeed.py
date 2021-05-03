#!/usr/bin/python
import time

from termcolor import colored
import ccxt


class CryptoLiveFeed:
    """Run a CryptoStrategy on a list of assets"""
    
    def __init__ (self, assets, strategy=None):
        self.assets = assets
        self.strategy = strategy

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

                    # TODO: is_open? should_open? BUY
                    # TODO: is_open? should_close? SELL

            print("[* LiveFeed] Finished iteration. Waiting...")
            time.sleep(vinterval)


if __name__ == "__main__":
    # Test class functions
    import json
    assets =  json.loads(open('data\\coins_coinbasepro.json', 'r').read())
    live_feed = CryptoLiveFeed(assets, strategy=None)
    live_feed.run()