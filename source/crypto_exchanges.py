#!/usr/bin/python
# crypto_get_tickers.py - retrieve tickers from different 
# exchanges.
#
# Use these functions to select exchanges to use for historical
# data fetching . Find exchange with  high volitility.

from datetime import datetime
import json

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


def get_exchanges (voutfile=None, vprint=True, vlist=None):
    # Retrieve metadata from exchanges. Optionally print to 
    # stdout and write to file. (binance, kraken, etc.)
    vres = []

    i = 0
    for vex in ccxt.exchanges:
        # Check exchange is in request list.
        if not vlist is None:
            if not vex in vlist: continue

        # Set limit here.
        # if i > 4: break
        i += 1

        print("[* exchanges] %s" % vex)
        try:
            # Get exchange data.
            exchange = getattr(ccxt, vex)()
            exchange.load_markets()
            vcoins_under = len(
                coins_in_range(exchange, 0, 0.50))

            # Print output.
            print("[* exchanges] Name: %s" % vex)
            print("[* exchanges] Size: %s" 
                   % len(exchange.symbols))
            print("[* exchanges] Coins under $0.50: %s"
                    % vcoins_under)
            print("")

            # Add to output struct.
            vres.append({
                "name": vex,
                "size": len(exchange.symbols),
                "coins_under_50_cents": vcoins_under
            })

        except Exception as e:
            print("[* exchanges] Could not load exchange %s."
                  % vex)
            print(e)
            print("")

    # Write out exchange information.
    print("[* exchanges] Total exchanges: %s" 
          % len(ccxt.exchanges))

    # Write sorted to output file.
    if voutfile:
        vres_sorted = sorted(vres, 
               key=lambda x: x['coins_under_50_cents'])
        vres_sorted.reverse()
        open(voutfile, 'w+').write(
            json.dumps(vres_sorted, indent=4))
        print("[* exchanges] Wrote out %s." % voutfile)

    return vres


def change_in_day (vex, vsymb):
    # Returns the change % of a symbol in past 24 hours.
    vres = 0
    return vres


def coins_in_range (vex, vmin, vmax):
    # Return the coins within a price range of an exchange.
    # vex should have market loaded already.
    vres = []
    for vsymb_text in vex.symbols:
        try:
            vbars = vex.fetch_ohlcv(vsymb_text)
            # Need to calc change percent 
            # from bar[0] and bar[-1]
            # DEBUG #
            print("%s : %s" % (vsymb_text, len(vbars)))
            vclose = vbars[-1][-2]
            if vclose < vmax and vclose > vmin:
                vres.append({
                    'symbol': vsymb_text,
                    'close': vclose
                })
        except Exception as e:
            # print("coins in range exception: %s" % e)
            continue

    return vres


# TODO: Move to crypto_coins.py
def get_coins (vexchange, vmin_price, vmax_price, vmin_change):
    # Get tickers which fall in a certain price range.
    # Retrieve all symbols as open price.
    # Save to designated JSON path.

    # Fetch symbols from exchange.
    exchange = getattr(ccxt, vexchange)()
    exchange.load_markets()

    # No symbols found.
    if len(exchange.symbols) == 0:
        print("[* tickers] No tickers found on"+
                " exchange %s." % sys.argv[1])
        sys.exit()

    print("[* tickers] found %s symbols." 
            % len(exchange.symbols))

    # Filter symbols by close price < $0.50
    vres = []
    for vsymb_text in exchange.symbols:
        try:
            vbars = exchange.fetch_ohlcv(vsymb_text)
        except Exception as e:
            print("[* crypto_get_tickers] Cannot fetch %s : %s" 
                    % (vsymb_text, e))
            continue

        print('[* crypto_get_tickers] Fetched symbol %s' 
                % vsymb_text)
        print("[* crypto_get_tickers] Num bars for %s: %s" 
                % (vsymb_text, len(vbars)))
        print()

        vdate = pd.to_datetime(vbars[0][0], unit='ms')
        vclose = vbars[-1][-2]
        # TODO: Get 24 hour change %.
        if vclose < 0.50: # && vchange % > 5
            vres.append({
                'symbol': vsymb_text,
                'timestamp': str(vdate),
                'close': vclose,
                'volume': vbars[-1][-1]
            })

    # Write out results.
    print("[* crypto_get_tickers] %s tickers downloaded." 
            % len(vres))
    vfname = "./data/tickers_%s.json" % vexchange
    open(vfname, 'w+').write(json.dumps(vres, indent=4))
