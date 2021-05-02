#!/usr/bin/python
# crypto_broker.py - Functions to connect to personal wallet
# and portfolio for an exchange or use paper wallet. The 
# wallet used in crypto-bot can be configured in the file
# `.crypto.json`.
# Implement BUY and SELL functions here.

import json

import ccxt


## Coinbase Broker #############################################
# Need to have your wallet info in a file ".crypto.json"
vkeys = json.loads(open(".crypto.json", 'r').read())

vex = getattr(ccxt, 'coinbase')({
    'apiKey': vkeys['cb-apikey'],
    'secret': vkeys['cb-secret'],
    'timeout': 30000,
    'enableRateLimit': True
})


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