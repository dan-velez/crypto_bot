#!/usr/bin/python
# crypto_bot.py - CLI for crypto trader scripts.

import sys
import argparse

import crypto_exchanges

"""
crypto_bot.py <command> [<args>]

COMMAND
    exchanges --outfile STRING
    exchanges size [ALL | STRING]
    backtest --hist_file STRING --strategy STRING
    tickers --exchange STRING --max_price FLOAT
    history --exchange STRING --symbol STRING --start STRING 
            --end STRING --dir STRING
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

    # By default, exchanges will show all exchanges with 
    # metadata (name, size, num coins under $0.50)
    vparser_exchanges = subparsers.add_parser(
        'exchanges',
        help='Download information on available exchanges.')

    vparser_exchanges.add_argument(
        '-o',
        '--outfile',
        required=False,
        help='Optionally output data as JSON to a file.')

    # Use tickers to further probe exchange prices.
    # Can input certain filters.
    vparser_tickers = subparsers.add_parser(
        'tickers',
        help='Download OHLCV data on tickers of an exchange.')

    vparser_tickers.add_argument(
        '-x',
        '--exchange',
        required=True,
        help='The exchange of which to download tickers.')

    # Select a file wit OPEN/CLOSE functions
    vparser_backtest = subparsers.add_parser(
        'backtest', 
        help='Backtest a strategy on historical data.')

    vparser_backtest.add_argument(
        'hist_file', 
        help='The JSON data of a ticker, previously generated.',
        type=str)

    # Parse args.
    # if len(sys.argv) < 3:
    #   parser.print_help(sys.stderr)
    #   sys.exit(1)

    vargs = parser.parse_args()

    try:
        # Run command.
        if vargs.command == "exchanges":
            print("[* bot] Fetching exchanges with metadata...")
            print()
            crypto_exchanges.get_exchanges(
                voutfile=vargs.outfile, vprint=True)
    except KeyboardInterrupt:
        print("[* bot] Exiting. Goodbye!")
        sys.exit(1)


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
