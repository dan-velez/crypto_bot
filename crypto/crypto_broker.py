#!/usr/bin/python
# crypto_broker.py - Functions to connect to exchanges and use
# trading functions. Maybe connect to wallet as well.

import json

import ccxt
# import crypto_exchanges
# crypto_exchanges.get_tickers('coinbase', 0, 0, 0)

vkeys = json.loads(open(".crypto.json", 'r').read())

vex = getattr(ccxt, 'coinbase')({
    'apiKey': vkeys['cb-apikey'],
    'secret': vkeys['cb-secret'],
    'timeout': 30000,
    'enableRateLimit': True
})

# Get coin from coinbase, and trade in alt coin.
# Use coinbase to trade FIAT to BTC.
# Then send to wallet. Try to do all crypto things via code.
# Add commands to crypto-bot
