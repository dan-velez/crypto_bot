#!/usr/bin/python3
# crypto_backtest.py - Backtest on historical data.

import json

vtrade_quantity = 10


def backtest (fnopen, fnclose, vhist):
    # Loop through bars
    # Test open / exit conditions on each

    for vbar in vhist:
        vsymb = vbar['symbol']
        print("[* crypto_backtest] %s @ %s" % (vsymb, vbar['close']))
        if is_open(vsymb):
            if should_close(): sell(vsymb, vtrade_quantity)

        else:
            if should_open(): buy(vsymb, vtrade_quantity)
    
    print(vportfolio_total)


## Paper Broker ################################################################

vportfolio = {
    'total_value': 100.00,
    'assets': []
}

def is_open (vsym):
    # Return true if there is an open position on this symbol.
    return False


def buy (vsym, vqty):
    # Open a position on symbol for vqty shares.
    return


def sell (vsym, vqty):
    # Sell certain amount asset through api.
    return


def port_has_asset ():
    # Return wether portfolio contains a certain asset
    return False


## Strategy ####################################################################

def should_open (vsymb, vhist):
    vhave = port_has_asset(vsymb)
    return False


def should_close (vsymb, vhist):
    return False


## CLI #########################################################################

if __name__ == "__main__":
    import sys

    # TODO: crypto_broker_paper.py , crypto_broker_live.py

    # TODO: Examine different market prices for same symbol
    # TODO: Keep hash table for fast lookup. Go down list of pairs. 
    # TODO: May need async, multiple threads

    if len(sys.argv) < 2:
        print("[*] Usage: crypto_backtest.py <symbol_history_file.json>")
        sys.exit()

    # Load history file
    vhist_file = sys.argv[1]
    vjson_hist = json.loads(open(vhist_file, 'r').read())
    print("[* crypto_backtest] %s bars available." % len(vjson_hist))
    backtest(should_open, should_close, vjson_hist)
