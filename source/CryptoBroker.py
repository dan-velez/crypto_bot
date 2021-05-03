#!/usr/bin/python

import json

import ccxt


class CryptoBroker:
    """This class implements functions to connect to personal wallet and 
    portfolio for an exchange or use paper wallet. 
    
    The wallet used in crypto-bot can be configured in the file `.crypto.json`. 
    Implement BUY and SELL functions here. The default broker is a PAPER broker.
    To use a broker for your own wallet/exchange, inherit this and use its API
    functions via CCXT. The PAPER broker holds its portfolio in memory and is 
    only used for testing."""

    def get_wallet ():
        """Get the wallet reference using ccxt."""
        vkeys = json.loads(open(".crypto.json", 'r').read())

        vex = getattr(ccxt, 'coinbase')({
            'apiKey': vkeys['cb-apikey'],
            'secret': vkeys['cb-secret'],
            'timeout': 30000,
            'enableRateLimit': True
        })

        vportfolio = {
            'total_value': 100.00,
            'assets': []
        }

    def is_open (self, vsym):
        """Return true if there is an open position on this symbol.
        I.e., if it exists in portfolio."""

        for vasset in vportfolio['assets']:
            if vasset['symbol'] == vsym: return True
        return False

    def buy (self, vsym, vqty):
        """Open a position on symbol for vqty shares."""
        
        vsym['quantity'] = vqty    
        vportfolio['assets'].append(vsym)
        vportfolio['total_value'] -= vsym['close'] * vqty
        return True

    def sell (self, vsym, vqty):
        """Sell certain amount asset through api.""""
        
        vtotal_sell = vsym['close'] * vqty
        for vasset in vportfolio['assets']:
            pass
        return True

    def port_total(self):
        """Returns total value of portfolio for this broker."""

        return vportfolio['total_value']