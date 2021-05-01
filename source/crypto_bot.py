#!/usr/bin/python
# crypto_bot.py - CLI for crypto trader scripts.
# Swiss army knife for crypto trading things.
# Probe exchanges and coin data from CLI.
# TODO: Implement coins command. Get ohlcv data for coins.
# TODO: Calculate change percent for given time frame.

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


def parser_subcommands ():
    # Arg parser with support for multiple sub commands.

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
        help='Download information on available exchanges.')

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
        help='Download OHLCV data on coins of an exchange.')

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

    except KeyboardInterrupt:
        print("[* bot] Exiting. Goodbye!")
        sys.exit(1)


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


def parser_tutorial ():
    # Arg parser created from official tutorial.

    vparser = argparse.ArgumentParser(
    description="Retrieve crypto data and run back"+
    " tests, live tests, and live trading.")

    vparser.add_argument(
        'command', 
        help='the command you want to run',
        choices=[
            'backtest',
            'tickers',
            'history',
            'exchanges'
        ])

    vparser.add_argument(
        'square',
        help='display square of number given',
        type=int)

    vparser.add_argument(
        '-v', 
        '--verbose',
        help='increase output verbosity', 
        action='store_true')

    vparser.add_argument(
        '-l',
        '--level',
        help='set verbosity level', 
        type=int, 
        choices=[0, 1, 2])

    vparser.add_argument(
        '-i',
        '--increase', 
        default=0,
        help='test count argument', 
        action='count')

    vargs = vparser.parse_args()

    # Run parser command with args.
    print("Done.")
    print(vargs.command)
    print(vargs.square**2)

    # Options
    if vargs.verbose:
        print("[*] All arguments parsed.")

    if vargs.level == 2: print('[*] level 2!')
    elif vargs.level == 1: print('[*] level 1!')
    else: print('[*] No level!')

    print(vargs.increase)


if __name__ == "__main__":
    # Run CLI
    parser_subcommands()
    # parser_tutorial()
