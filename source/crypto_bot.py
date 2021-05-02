#!/usr/bin/python
# crypto_bot.py - CLI for crypto trader tasks.
# Swiss army knife for crypto trading things.
# View and download exchanges and coin data.

import sys
import argparse

import crypto_exchanges

"""
crypto_bot.py <command> [<args>]

COMMAND
    exchanges --outfile STRING
    exchanges size [ALL | STRING]
    coins --exchange STRING --max_price FLOAT

    broker --buy <COIN> <VOLUME>
    broker --sell <COIN> <VOLUME>
    history --exchange STRING --symbol STRING --start STRING 
            --end STRING --dir STRING
    backtest --hist_file STRING --strategy STRING
"""


def crypto_bot_cli ():
    # crypt-bot CLI parser for all sub commands.

    parser = argparse.ArgumentParser(
        prog="crypto-bot",
        description="Retrieve crypto data and run back"+
        " tests, live tests, and live trading.",
        epilog="crypto-bot <command> -h displays help on a "+
               "particular command.")

    subparsers = parser.add_subparsers(
        help='Command',
        dest='command')

    ## Exchanges ###############################################
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

    ## Coins ###################################################
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

    ## Backtest ################################################
    # Select a file wit OPEN/CLOSE functions
    vparser_backtest = subparsers.add_parser(
        'backtest', 
        help='Backtest a strategy on historical data.')

    vparser_backtest.add_argument(
        'hist_file', 
        help='The JSON data of a coin, previously generated.',
        type=str)

    ## Parse args ##############################################
    vargs = parser.parse_args()

    try:
        # Run command.
        if vargs.command ==   "exchanges": run_command_exchanges(vargs)
        elif vargs.command == "coins": pass
        elif vargs.command == "history": pass
        elif vargs.command == "backtest": pass
        elif vargs.command == "broker": pass
        elif vargs.command == "run": pass
        else: parser.print_help(sys.stderr)

    except KeyboardInterrupt:
        print("[* bot] Exiting. Goodbye!")
        sys.exit(1)


## Sub commands ################################################

def run_command_exchanges (vargs):
    # Run the exchanges command with arguments.
    print("[* bot] Get exchange data...")
    print()

    # Parse input list
    if not vargs.list is None:
        vargs.list = vargs.list.split(",")
        vargs.list = list(map(lambda x: x.strip(), vargs.list))

    if not vargs.size is None:
        # Just get size of an exchange.
        crypto_exchanges.exchange_size(vargs.size)

    else:
        # Retrieve all exchange data.
        # May take hours to complete.
        crypto_exchanges.get_exchanges(
            vlist=vargs.list,
            voutfile=vargs.outfile, vprint=True)


if __name__ == "__main__":
    # Run CLI
    crypto_bot_cli()
