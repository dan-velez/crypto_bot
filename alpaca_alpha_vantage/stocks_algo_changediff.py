# stocks_algo_changediff.py - Trade based on increase/decrease percentage throughout day.

from termcolor import colored

import stocks_get as pstocks
import stocks_alert as stalert
from stocks_broker import *
from stocks_structs import *
from stocks_report import *

import time
import json
import sys


## Main bot loop ###############################################################

def stock_monitor(vinterval=2, valert=False):
    "Monitor stocks for buy/sell indicators."

    # Buy params
    vchange_thresh = 7      # Spike tell
    vinvest_amount = 10.00   # How much to invest in each buy. 

    # Sell params
    vstop_loss     = -80   # Percentage of drop before sell. Never lose more than this.
    vsell_increase = 1    # Percentage to sell at

    while True:
        # Monitor stocks to buy. Need to divide requests by batches of 200.

        print("\n[* stock_mon] Sending batch of requests...")
        for vrow in VTICKERS:
            try:
    
                # Get Gain/Loss percentage from day start.
                vstart_price = float(vrow['Price'])
                vcurrent = alpaca_get_ticker_price(vrow['Symbol'])
                vchange = round((100 / vstart_price) * (vcurrent - vstart_price))
                if vchange > 0: vcolor = "green"
                else: vcolor = "red" 

                print("[* stock_mon] Check symbol BUY: %s" % colored(vrow['Symbol'], "cyan"))
                print("[* stock_mon] Day Start: %s" % colored(vstart_price, "yellow"))
                print("[* stock_mon] Current: %s" % vcurrent)
                print("[* stock_mon] Change %%: %s" % colored(vchange, vcolor))
                
                if vchange >= vchange_thresh:
                    if not has_investment(vrow["Symbol"]):
                        if valert: stalert.alert(vrow['Symbol'], "BUY", vchange, vcurrent)
                        ## Make BUY request here ##
                        ## Add to Investments    ##
                        ###########################
                        vshares = round(vinvest_amount / vcurrent)
                        print("\n[* stock_mon] " + colored("Buy %s shares of %s at %s" % (vshares, vrow['Symbol'], vcurrent), "green"))
                        # time.sleep(1.5)
                        alpaca_buy_stock(vrow['Symbol'], vshares)
                        # time.sleep(3)
                
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print("[* stock_mon] " + colored("Could not check stock: %s" % e, "red"))
                print("[* stock mon] " + colored("%s %s" % (exc_type, exc_tb.tb_lineno), "red"))

            print("")

        # Monitor selling point for investments.
        # Store last change % to measure drop from last check.
        print("\n[* stock_mon] "+ colored("Check portfolio for selling points...", "cyan"))
        time.sleep(7)

        for vrow_inv in VPORTFOLIO:
            
            print("[* stock_mon] Check investment: %s" % colored(vrow_inv['symbol'], "cyan"))

            # Alert when buy_price stock drops 7% **FROM LAST CHECK**
            vbuy_price = float(vrow_inv['buy_price'])
            vlast_price = float(vrow_inv['last_price'])
            vcurrent = alpaca_get_ticker_price(vrow_inv['symbol'])

            # Current price is new last price
            investments_update_last_price(vrow_inv['symbol'], vcurrent)

            # Calculate change from last price and buy price.
            vchange = ((float(vcurrent)-vlast_price)/vlast_price)*100
            vchange_buy = ((float(vcurrent)-vbuy_price)/vbuy_price)*100

            if vchange >= 0: vcolor = "green"
            else: vcolor = "red"

            if vchange_buy >= 0: vcolor2 = "green"
            else: vcolor2 = "red"

            print("[* stock_mon] Bought at: %s" % colored(vbuy_price, "yellow"))
            print("[* stock_mon] Previous Interval: %s" % vlast_price)
            print("[* stock_mon] Current: %s" % vcurrent)
            print("[* stock_mon] Change From Previous: %s" % colored(vchange, vcolor))
            print("[* stock_mon] Change From Buy: %s" % colored(vchange_buy, vcolor2))

            if (vchange <= vstop_loss) or (vchange_buy >= vsell_increase) or (vchange_buy <= vstop_loss):
                # TODO: Update start price after a sale, to prevent buying again.
                # TODO: Prevent short sale

                if valert: stalert.alert(vrow_inv['symbol'], "SELL", vchange, vcurrent)
                ## Make SELL request here  ##
                ## Remove from Investments ##
                #############################
                alpaca_sell_stock(vrow_inv['symbol'])
        
            print("")

        # Wait some time before checking again.
        print("[* stock_mon] " + colored("Wait for next interval...", "cyan"))
        time.sleep(vinterval*60)


## Main ########################################################################

if __name__ == "__main__":
    print(colored("== stock_monitor "+"="*48, "blue"))
    """
    print(colored("Hello World", "red"))
    print(colored("Hello World", "blue"))
    print(colored("Hello World", "yellow"))
    print(colored("Hello World", "green"))
    print(colored("Hello World", "cyan"))
    print(colored("Hello World", "magenta"))
    sys.exit()
    """

    if len(sys.argv) < 2:
        print(colored("usage: stock_monitor.py <check interval in minutes>", "cyan"))
        sys.exit()
    
    vinterval = sys.argv[1] # Sleep time in minutes.

    try:
        stock_monitor(int(vinterval))
    except KeyboardInterrupt as e:
        print("[* stock_mon] " + colored("Exiting stock bot...", "cyan"))
        report_main()
        sys.exit()

# TODO: Highlight 'current' price
# TODO: liquidate function
# TODO: Use MACD, when stock is up 4% from yestardays close, and has increased as well today (for more stable stocks)
# TODO: If sold short, you dont own it. Remove from portfolio.
#       - TODO: Check portfolio
# TODO: Test with stop loss at -7 and stop loss at -1 (record time when change stop loss, add to report)