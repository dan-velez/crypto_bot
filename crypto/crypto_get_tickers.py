#!/usr/bin/python3
# crypto_get_tickers.py - retrieve tickers from different exchanges.
# TODO: 
#   Retrieve full name of currencys
#   Read more about what crypto trading is, blockchain, and what are
#   cryptocurrencies.

from datetime import datetime
import json

import ccxt
import pandas as pd

# Login to Binance using API Key. Use in broker.
# from variable id
# exchange_id = 'binance'
# exchange_class = getattr(ccxt, exchange_id)
# exchange = exchange_class({
#     'apiKey': 'YOUR_API_KEY',
#     'secret': 'YOUR_SECRET',
#     'timeout': 30000,
#     'enableRateLimit': True,
# })


def print_exchange_sizes ():
    for vex in ccxt.exchanges:
        try:
            exchange = getattr(ccxt, vex)()
            # exchange = getattr(ccxt, 'binance')()
            # exchange = getattr(ccxt, 'kraken')()
            exchange.load_markets()
            # print(exchange.symbols)
            print("%s\t\t%s" % (vex, len(exchange.symbols)))
        except Exception as e:
            print("[*] Could not load exchange %s." % vex)


def get_tickers (vexchange, vmax_price, vmin_change, vsave=True):
    # Retrieve all symbols as open price.
    # Save to designated JSON path.
    return


def change_in_day (vsymb):
    # Returns the change % of a symbol in past 24 hours.
    vres = 0
    return vres


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("[*] Usage: crypto_get_tickers <EXCHANGE NAME>")
        sys.exit()

    # Fetch symbols from exchange.
    exchange = getattr(ccxt, sys.argv[1])()
    exchange.load_markets()
    if len(exchange.symbols) == 0:
        print("[* crypto_get_tickers] No tickers found on exchange %s." 
                % sys.argv[1])
        sys.exit()
    print("[* crypto_get_tickers] found %s symbols." % len(exchange.symbols))

    # Filter symbols by close price < $0.50
    vres = []
    for vsymb_text in exchange.symbols:
        try:
            vbars = exchange.fetch_ohlcv(vsymb_text)
        except Exception as e:
            print("[* crypto_get_tickers] Cannot fetch %s : %s" 
                    % (vsymb_text, e))
            continue

        print('[* crypto_get_tickers] Fetched symbol %s' % vsymb_text)
        print("[* crypto_get_tickers] Num bars for %s: %s" % (vsymb_text, len(vbars)))
        print()

        vdate = pd.to_datetime(vbars[0][0], unit='ms')
        vclose = vbars[0][-2]
        # TODO: Get 24 hour change %.
        if vclose < 0.50: # && vchange % > 5
            vres.append({
                'symbol': vsymb_text,
                'timestamp': str(vdate),
                'close': vclose
            })

    # Write out results.
    print("[* crypto_get_tickers] %s tickers downloaded." % len(vres))
    vfname = "./data/tickers_%s.json" % sys.argv[1]
    open(vfname, 'w+').write(json.dumps(vres, indent=4))

