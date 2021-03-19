# crypto_get_tickers.py - retrieve tickers from different exchanges.
# TODO: Parse as JSON instead of plain text.

import ccxt
from datetime import datetime
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


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("[*] Usage: crypto_get_tickers <EXCHANGE NAME>")
        sys.exit()


    exchange = getattr(ccxt, sys.argv[1])()
    exchange.load_markets()

    # Filter symbols by close price < $0.50
    for vsymb_text in exchange.symbols:
        vsymb = exchange.fetch_ohlcv(vsymb_text)
        vdate = pd.to_datetime(vsymb[0][0], unit='ms')
        vclose = vsymb[0][-2]
        if vclose < 0.50:
            print(vsymb_text)
            print(vdate)
            print(vclose)
            print()

    # print(len(exchange.symbols))