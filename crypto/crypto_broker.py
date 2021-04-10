#!/usr/bin/python
# crypto_broker.py - Functions to connect to exchanges and use
# trading functions. Maybe connect to wallet as well.

import json

import ccxt
# import crypto_exchanges
# crypto_exchanges.get_tickers('coinbase', 0, 0, 0)

vkeys = json.loads(open("/home/danie/.crypto.json", 'r').read())

def x ():
    vex = getattr(ccxt, 'coinbase')({
        'apiKey': '',
        'secret': '',
        'timeout': 30000,
        'enableRateLimit': True
    })


# Get coin from coinbase, and trade in alt coin.
# Use coinbase to trade FIAT to BTC.
# Then send to wallet. Try to do all crypto things via code.
# Add commands to crypto-bot
