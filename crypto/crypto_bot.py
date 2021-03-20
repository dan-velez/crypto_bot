#!/usr/bin/python
# crypto_bot.py - CLI for crypto trader scripts.

"""
crypto_bot.py COMMAND OPTIONS

COMMAND
    exchanges --outfile STRING
    exchanges size [ALL | STRING]
    backtest --hist_file STRING
    tickers --exchange STRING --max_price FLOAT
    history --exchange STRING --symbol STRING --start STRING --end STRING --dir STRING
"""


def parser_subcommands ():
    # Arg parser with support for multiple sub commands.
    import argparse
    parser = argparse.ArgumentParser(
        description="Retrieve crypto data and run back tests, live tests, and live trading."
    )
    subparsers = parser.add_subparsers(help='Functions')
    
    parser_1 = subparsers.add_parser('backtest', help='...')
    parser_1.add_argument('cmd1_option1', type=str, help='...')
    parser_1.set_defaults(backtest=True)

    parser_2 = subparsers.add_parser('exchanges', help='...')
    parser_2.set_defaults(exchanges=True)

    parser_3 = subparsers.add_parser('tickers', help='...')
    parser_3.add_argument('cmd3_options', type=int, help='...')
    parser_3.set_defaults(tickers=True)

    args = parser.parse_args()
    print(args)


def parser_tutorial ():
    # Arg parser created from official tutorial.
    import argparse
    vparser = argparse.ArgumentParser(
        description="Retrieve crypto data and run back tests, live tests, and live trading."
    )

    vparser.add_argument('command', help='the command you want to run',
        choices=[
            'backtest',
            'tickers',
            'history',
            'exchanges'
        ])

    vparser.add_argument('square', help='display square of number given', type=int)
    
    vparser.add_argument('-v', '--verbose', help='increase output verbosity', 
        action='store_true')
    
    vparser.add_argument('-l', '--level', help='set verbosity level', 
        type=int, choices=[0, 1, 2])
    
    vparser.add_argument('-i', '--increase', 
        default=0, help='test count argument', action='count')


    vargs = vparser.parse_args()
    print(vargs.command)
    print(vargs.square**2)
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
