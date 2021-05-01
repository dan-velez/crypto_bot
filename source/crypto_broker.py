#!/usr/bin/python
# crypto_broker.py - Functions to connect to exchanges and use
# trading functions. Maybe connect to wallet as well.
# Implement BUY and SELL functions here.

import json

import ccxt
# import crypto_exchanges
# crypto_exchanges.get_tickers('coinbase', 0, 0, 0)

# Need to have your wallet info in a file ".crypto.json"
vkeys = json.loads(open(".crypto.json", 'r').read())

vex = getattr(ccxt, 'coinbase')({
    'apiKey': vkeys['cb-apikey'],
    'secret': vkeys['cb-secret'],
    'timeout': 30000,
    'enableRateLimit': True
})