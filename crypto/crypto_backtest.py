#!/usr/bin/python
# crypto_backtest.py - Backtest on historical data.

import json

from termcolor import colored

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


## Paper Broker ################################################

vportfolio = {
    'total_value': 100.00,
    'assets': []
}

def is_open (vsym):
    # Return true if there is an open position on this symbol.
    # I.e., if it exists in portfolio.
    for vasset in vportfolio['assets']:
        if vasset['symbol'] == vsym: return True
    return False


def buy (vsym, vqty):
    # Open a position on symbol for vqty shares.
    vsym['quantity'] = vqty    
    vportfolio['assets'].append(vsym)
    vportfolio['total_value'] -= vsym['close'] * vqty
    return True


def sell (vsym, vqty):
    # Sell certain amount asset through api.
    vtotal_sell = vsym['close'] * vqty
    for vasset in vportfolio['assets']:
        pass
    return True


def port_total():
    # Returns total value of portfolio for this broker.
    return vportfolio['total_value']


## Strategy ####################################################

def should_open (vbar, vhist):
    # Open if:
    #     change_percent from day_open > 5
    #     not currently open
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

    # TODO: crypto_broker_paper.py , crypto_broker_live.py
    # TODO: Examine different market prices for same symbol
    # TODO: Keep hash table for fast lookup. 
    #   Go down list of pairs. 
    # TODO: May need async, multiple threads

    if len(sys.argv) < 2:
        print("[*] Usage: crypto_backtest.py "+
                "<symbol_history_file.json>")
        sys.exit()

    # Load history file
    vhist_file = sys.argv[1]
    vjson_hist = json.loads(open(vhist_file, 'r').read())
    print("[* crypto_backtest] %s bars available." %
            len(vjson_hist['history']))
    backtest(should_open, should_close, vjson_hist)
