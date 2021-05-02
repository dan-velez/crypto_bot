#!/usr/bin/python
# crypto_get_tickers.py - retrieve tickers from different 
# exchanges.
#
# Use these functions to select exchanges to use for historical
# data fetching . Find exchange with  high volitility.

from datetime import datetime
import json
import time

import ccxt
import pandas as pd
from termcolor import colored


def exchange_size (vex):
    # Prints the size of an exchange.
    exchange = getattr(ccxt, vex)()
    exchange.load_markets()
    vlen = len(exchange.symbols)
    print("[* exchanges] %s has %s coins available." 
        % (vex, vlen))
    return vlen


def get_exchanges (voutfile=None, vprint=True, vlist=None, 
                   vsize_limit=None):
    # Retrieve metadata from exchanges. Optionally print to 
    # stdout and write to file. (binance, kraken, etc.)
    vres = []

    for vex in ccxt.exchanges:
        # Check exchange is in request list.
        if not vlist is None:
            if not vex in vlist: continue

        try:
            # Get exchange data.
            exchange = getattr(ccxt, vex)()
            exchange.load_markets()
            
            # Check if there is a size limit given.
            if vsize_limit:
                if len(exchange.symbols) > vsize_limit: continue
            
            # Continue to get exchange asset data.
            print("\n[* exchanges] %s" % vex)
            vcoins = get_coins(exchange, vname=vex)

            # Print output.
            print("[* exchanges] Size: %s" 
                   % len(exchange.symbols))
            print("")

            # Add to output struct.
            vres.append({
                "name": vex,
                "size": len(exchange.symbols),
                "coins": vcoins
            })

        except Exception as e:
            print("[* exchanges] Could not load exchange %s."
                  % vex)
            # print(e)
            print("")

    # Write out exchange information.
    print("[* exchanges] Total exchanges: %s" 
          % len(ccxt.exchanges))

    # Write sorted to output file.
    if voutfile:
        vres_sorted = sorted(vres, 
               key=lambda x: x['size'])
        vres_sorted.reverse()
        open(voutfile, 'w+').write(
            json.dumps(vres_sorted, indent=4))
        print("[* exchanges] Wrote out %s." % voutfile)

    return vres


def change_in_24_hours (vex, vsymb):
    # Returns the change % of a symbol in past 24 hours.
    vres = 0
    return vres


def get_coins (vex, vname='', vrange=False, vmin=0, vmax=100):
    # Return the coins within a price range of an exchange.
    # vex should have market loaded already.
    vres = []
    for vsymb_text in vex.symbols:
        try:
            vbars = vex.fetch_ohlcv(vsymb_text)
            # Need to calc change percent 
            # from bar[0] and bar[-1]
            # DEBUG # len(vbars)
            vclose = vbars[-1][-2]
            print("%s : $%s" % (vsymb_text, vclose))

            # Check for asset price range setting.
            vappend = True
            if vrange and vclose > vmax and vclose < vmin: 
                vappend = False

            # Add to final JSON.
            if vappend:
                vres.append({
                    'symbol': vsymb_text,
                    'close': vclose
                })
            
            # Limit requests for coinbasepro public API.
            if vname == 'coinbasepro': time.sleep(0.25)
        except Exception as e:
            print("[* exchanges] Cant get coin %s" 
                % (vsymb_text)) 
            continue

    return vres