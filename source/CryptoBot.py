#!/usr/bin/python

import sys
import argparse

from CryptoExchanges import CryptoExchanges
from CryptoCoins import CryptoCoins


class CryptoBot:
    """crypto-bot CLI tool for automatin crypto trading tasks.

    Swiss army knife for crypto trading things. View and download exchanges and 
    coin data. Run backtests on historical data and live feed."""

    # Sub command objects
    vexchanges = CryptoExchanges()
    vcoins = CryptoCoins()


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
            elif vargs.command == "coins": pass
            elif vargs.command == "history": pass
            elif vargs.command == "backtest": pass
            elif vargs.command == "broker": pass
            elif vargs.command == "run": pass
            else: parser.print_help(sys.stderr)

        except KeyboardInterrupt:
            print("\n[* CryptoBot] Exiting. Goodbye!")
            sys.exit(1)

    ## Sub commands ############################################################

    def run_command_coins (self, vargs):
        return

    def run_command_exchanges (self, vargs):
        """Run the exchanges command with user input arguments."""

        print("[* CryptoBot] Get exchange data...")
        print()

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