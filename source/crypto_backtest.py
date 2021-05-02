#!/usr/bin/python
# crypto_backtest.py - Backtest on historical data.
# TODO: move strategy to own file, factor out CLI part.

import json

from termcolor import colored

from crypto_broker import is_open

vtrade_quantity = 10


def backtest (fnopen, fnclose, vhist):
    # Loop through bars
    # Test open / exit conditions on each
    print("[* crypto_backtest] Period Start Price: %s" %
            vhist['initial'])
    print()

    for vbar in vhist['history']:
        vsymb = vbar['symbol']
        print("[* crypto_backtest] %s @ %s" % 
                (vsymb, vbar['close']))
        if is_open(vsymb):
            if should_close(): sell(vsymb, vtrade_quantity)
        else:
            if should_open(vbar, vhist):
                buy(vsymb, vtrade_quantity)
    
    print(port_total())


## Strategy ####################################################

def should_open (vbar, vhist):
    # Open if:
    #     change_percent from day_open > 5.
    #     not currently open.
    #     has enough volume to perform trade.
    vchange = vbar['close'] - vhist['initial']
    vchange_percent = round(
            (vchange / vhist['initial']) * 100, 2)

    # Print debug info.
    if vchange_percent > 0: vcolor = 'green'
    else: vcolor = 'red'
    print(colored(
        "[* crypto_backtest] change since open: %s%%" % 
        vchange_percent, vcolor))
    print('')
    return False


def should_close (vsymb, vhist):
    # Close if:
    #   change_percent since buy price < -5
    #   Take 5% loss
    #   OR if change % > 5
    #   Take 5% profit
    return False


## CLI #########################################################

if __name__ == "__main__":
    import sys

    # TODO: crypto_broker_paper.py , crypto_broker.py

    if len(sys.argv) < 2:
        print("[*] Usage: crypto_backtest.py "+
                "<symbol_history_file.json>")
        sys.exit()

    # Load history file
    vhist_file = sys.argv[1]
    vjson_hist = json.loads(open(vhist_file, 'r').read())
    print("[* crypto_backtest] %s bars available." %
            len(vjson_hist['history']))

    # Run backtest with open / close signals.
    backtest(should_open, should_close, vjson_hist)
