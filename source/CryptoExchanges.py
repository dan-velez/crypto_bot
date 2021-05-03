#!/usr/bin/python

from datetime import datetime
import json
import time

import ccxt
from termcolor import colored

from CryptoCoins import CryptoCoins


class CryptoExchanges:
    """Retrieve data on exchanges such as size and available assets.
    Used to download lists of coin pairs.""" 

    # Use the coins object to get OHLCV data of assets.
    vcoins = CryptoCoins()

    def exchange_size (self, vex):
        """Gets the total number of assets in an exchange."""

        exchange = getattr(ccxt, vex)()
        exchange.load_markets()
        vlen = len(exchange.symbols)
        print("[* Exchanges] %s has %s coins available." % (vex, vlen))
        return vlen

    def get_exchanges (self, voutfile=None, vprint=True, vlist=None, 
                    vsize_limit=None):
        """Retrieve list of exchanges and a sublist of assets in exchange. 
        Optionally print to stdout and write to file."""
        
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
                print(colored("\n[* Exchanges] %s" % vex, 'blue'))
                vcoins = self.get_coins(exchange, vname=vex)

                # Print output.
                print("[* Exchanges] Size: %s\n" % len(exchange.symbols))

                # Add to output struct.
                vres.append({
                    "name": vex,
                    "size": len(exchange.symbols),
                    "coins": vcoins
                })

            except Exception as e:
                print(colored("[* Exchanges] Could not load exchange %s."
                    % vex, 'red'))
                # print(e)
                print("")

        # Write out exchange information.
        print("[* Exchanges] Total exchanges: %s" % len(ccxt.exchanges))

        # Write sorted to output file.
        if voutfile:
            vres_sorted = sorted(vres, key=lambda x: x['size'])
            vres_sorted.reverse()
            open(voutfile, 'w+').write(json.dumps(vres_sorted, indent=4))
            print("[* Exchanges] Wrote out %s." % voutfile)

        return vres

    def change_in_24_hours (self, vex, vsymb):
        """Returns the change % of a symbol in past 24 hours."""
        vres = 0
        return vres

    def get_coins (self, vex, vname='', vrange=False, vmin=0, vmax=100):
        """Return the coins within a price range of an exchange.
        vex should have market loaded already."""

        vres = []

        for vsymb_text in vex.symbols:
            try:
                # Get bars data. 
                vbars = vex.fetch_ohlcv(vsymb_text)
                vclose = vbars[-1][-2]
                vvolatil = self.vcoins.volatility_24_hour(vex, vsymb_text)
                
                # Print asset info to terminal.
                if vvolatil < 0: vcolor = 'red'
                else: vcolor = 'green'

                print(colored("[* Exchanges] %s : $%s : %s%%" % 
                    (vsymb_text, vclose, colored(vvolatil, vcolor)), 'cyan'))

                # Check for asset price range setting.
                vappend = True
                if vrange and vclose > vmax and vclose < vmin: 
                    vappend = False

                # Add to final JSON.
                if vappend:
                    vres.append({
                        'symbol': vsymb_text,
                        'close': vclose,
                        'volatility': vvolatil
                    })
                
                # Limit requests for coinbasepro public API.
                if vname == 'coinbasepro': time.sleep(0.25)
                # time.sleep(binance.rateLimit / 1000)
            except Exception as e:
                print(colored("[* Exchanges] Cant get coin %s" 
                    % (vsymb_text), 'red')) 
                # print(e)
                continue

        return vres