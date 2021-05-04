#!/usr/bin/python

import sys
import argparse
import json

from termcolor import colored

from crypto_bot.CryptoExchanges import CryptoExchanges
from CryptoCoins import CryptoCoins
from CryptoLiveFeed import CryptoLiveFeed


class CryptoBot:
    """crypto-bot CLI tool for automatin crypto trading tasks.

    Swiss army knife for crypto trading things. View and download exchanges and 
    coin data. Run backtests on historical data and live feed."""

    # Sub command objects
    vexchanges = CryptoExchanges()
    vcoins = CryptoCoins()
    vfeed = None


    def run_cli (self):
        """crypt-bot CLI parser for all sub commands."""

        parser = argparse.ArgumentParser(
            prog="crypto-bot",
            description="Retrieve crypto data and run back"+
            " tests, live tests, and live trading.",
            epilog="crypto-bot <command> -h displays help on a "+
                "particular command.")

        subparsers = parser.add_subparsers(
            help='Command',
            dest='command')

        ## Exchanges ###########################################################
        # By default, exchanges will show all exchanges with 
        # metadata (name, size, num coins under $0.50)
        vparser_exchanges = subparsers.add_parser(
            'exchanges',
            help='View / download information on available exchanges.')

        vparser_exchanges.add_argument(
            '-l',
            '--list',
            type=str,
            required=False,
            help='Quoted, comma seperated list of names of '+
                'exchanges to fetch.')

        vparser_exchanges.add_argument(
            '-sl',
            '--size-limit',
            type=int,
            required=False,
            help='Only fetch exchanges which contain a max of '+
                'this number of coins.')

        vparser_exchanges.add_argument(
            '-s',
            '--size',
            type=str,
            required=False,
            help='Get size of an exchange.')

        vparser_exchanges.add_argument(
            '-o',
            '--outfile',
            type=str,
            required=False,
            help='Optionally output data as JSON to a file.')

        ## Run #################################################################
        # Run LiveFeed with an assets list and strategy class.
        vparser_run = subparsers.add_parser(
            'run', 
            help='Run live ticker feed on an assets list '
                 +'with a strategy class.')

        vparser_run.add_argument(
            '-a',
            '--assets', 
            help='A list of assets to run the live ticker feed on. Should be '+ 
                 'a JSON file generated with the exchanges command.',
            required=True,
            type=str)
        
        vparser_run.add_argument(
            '-i',
            '--interval',
            help='How many seconds the bot should sleep in between loops over '+
                 'the entire assets list.',
            required=False,
            default=5,
            type=int)

        ## Coins ###############################################################
        # Use coins to further probe exchange prices.
        # Can input certain filters.
        vparser_coins = subparsers.add_parser(
            'coins',
            help='View / download OHLCV data on coins of an exchange.')

        vparser_coins.add_argument(
            '-x',
            '--exchange',
            required=True,
            type=str,
            help='The exchange of which to download coin prices.')

        ## Backtest ############################################################
        # Select a file wit OPEN/CLOSE functions
        vparser_backtest = subparsers.add_parser(
            'backtest', 
            help='Backtest a strategy on historical data.')

        vparser_backtest.add_argument(
            'hist_file', 
            help='The JSON data of a coin, previously generated.',
            type=str)

        ## Parse args ##########################################################
        vargs = parser.parse_args()

        try:
            # Run command.
            if vargs.command ==   "exchanges": self.run_command_exchanges(vargs)
            elif vargs.command == "run": self.run_command_run(vargs)
            elif vargs.command == "coins": pass
            elif vargs.command == "backtest": pass
            elif vargs.command == "broker": pass
            else: parser.print_help(sys.stderr)

        except KeyboardInterrupt:
            print("\n[* Bot] Exiting. Goodbye!")
            sys.exit(1)

    ## Sub commands ############################################################

    def run_command_run (self, vargs):
        """Run the live ticker feed on an assets list and strategy class."""
        
        print("[* Bot] Run live ticker feed and strategy...\n")
        try:
            vassets = json.loads(open(vargs.assets, 'r').read())
        except:
            print(colored("[* Bot] Invalid assets file!", 'red'))
            sys.exit(1)
        
        # TEMP: Use default strategy and broker
        from CryptoStrategy import CryptoStrategy
        from CryptoBroker import CryptoBroker
        self.feed = CryptoLiveFeed(
            assets=vassets, strategy=CryptoStrategy(), broker=CryptoBroker())
        self.feed.run(vinterval=vargs.interval)

    def run_command_exchanges (self, vargs):
        """Run the exchanges command with user input arguments."""

        print("[* Bot] Get assets list...\n")

        # Parse input list
        if not vargs.list is None:
            vargs.list = vargs.list.split(",")
            vargs.list = list(map(lambda x: x.strip(), vargs.list))

        if not vargs.size is None:
            # Just get size of an exchange.
            self.vexchanges.exchange_size(vargs.size)

        else:
            # Retrieve all exchange data.
            # May take hours to complete.
            self.vexchanges.get_exchanges(
                vlist=vargs.list,
                voutfile=vargs.outfile,
                vsize_limit=vargs.size_limit,
                vprint=True)


if __name__ == "__main__":
    # Instantiate new CryptoBot and run its CLI.
    CryptoBot().run_cli()