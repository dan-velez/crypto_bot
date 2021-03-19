# stocks_broker.py - Functions that access the brokerage API.

import alpaca_trade_api as tradeapi
from termcolor import colored
import time
import datetime

# Import persistant structs that bot uses.
from stocks_structs import *

# Init API

# Paper
# api_key = 'PK7UJ5HH6VUOFKY6Y9N7'
# base_url = 'https://paper-api.alpaca.markets'

# Live
api_key = 'AKUCM4NWNSY44F6OQYEG' # Live
base_url = 'https://api.alpaca.markets'

api_secret = '0KargnXyhjJEJyNWAA5bnwF6MPXeRmUL1EnSoY56'
# vapi = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
vapi = tradeapi.REST(api_key, api_secret, base_url)
# vapi = tradeapi.REST()


## Aplaca Wrappers ############################################################

def alpaca_buy_stock(vname, vshares):
    # Use Aplaca API to buy a stock by symbol name.
    try: 
        print("[* stock_mon] Submit order...")

        vapi.submit_order(
            symbol=vname,
            qty=vshares,
            side='buy',
            type='market',
            time_in_force='day')

        print("[* stock_mon] Get buy price...")

        # Get buy price from API.
        vbuy_price = float(vapi.polygon.last_quote(vname).askprice)

        # Retrieve start price data.
        print("[* stock_mon] Get pstock...")
        vpstock = get_pstock(vname)

        # Add to investment struct.
        print("[* stock_mon] Add investment...")
        # symbol, start_price, buy_price, shares, last_price

        add_investment(vname, vpstock["Price"], vbuy_price, vshares, vbuy_price)
    except Exception as e: 
        print("[* stock_mon] "+ colored("ERROR: Could not buy stock [%s]" % e, 'red'))


def alpaca_sell_stock(vname):
    # Use Aplaca API to sell a stock by symbol name.
    global VGAINS, VTICKERS

    # Get num shares from VPORTFOLIO struct.
    vinv = get_investment(vname)

    try:
        vapi.submit_order(
            symbol=vname,
            qty=int(vinv["shares"]),
            side='sell',
            type='market',
            time_in_force='day')
    except Exception as e:
        print("[* stock_mon] "+ colored("ERROR Could not sell %s. API error: %s" % (vname, e), "red"))
        return

    vbuy = float(vinv["buy_price"])
    vsell = float(vinv["last_price"])
    vchange_percent = ((float(vsell)-vbuy)/vbuy)*100

    print("[* stock_mon] Sold %s shares of %s. Gain/Loss: [%s]" % (vinv["shares"], vname, vchange_percent))
    time.sleep(3)
    
    # Track the gain/loss of sell.
    VGAINS.append({
        "symbol": vname, 
        "buy_price": vbuy, 
        "sell_price": vsell, 
        "gain %": vchange_percent,
        "time": str(datetime.datetime.now())  
    })
    open(VGAINS_FILE, "w").write(json.dumps(VGAINS, indent=4))

    # Set new start price in tickers file.
    for vrow in VTICKERS:
        if vrow['Symbol'] == vname:
            vrow['Price'] = vsell
            open(VTICKERS_FILE, "w").write(json.dumps(VTICKERS, indent=4))

    # Remove from VPORTFOLIO struct.
    remove_investment(vname)


## Indicators ##################################################################

def ind_moving_average(vsymb, vdays):
    # Return simple moving average indicator for a given symbol and number of days.
    # This method uses Alpaca's Alpha Vantage module. 100 requests per minute, 500/day.
    
    try:
        vsma = vapi.alpha_vantage.techindicators(
            symbol=vsymb, interval='weekly', 
            time_period=str(vdays), series_type='close')

        # print(json.dumps(vsma, indent=4))
        if 'Note' in vsma.keys():
            print("[* stocks_broker] ERROR while getting SMA for [%s]. %s" % (vsymb, vsma['Note']))
            return 0.0
        else:
            vkey = list(vsma['Technical Analysis: SMA'].keys())[0]
            vres = float(vsma['Technical Analysis: SMA'][vkey]['SMA'])
            return vres

    except Exception as e:
        print("[* stocks_broker] "+ colored("ERROR: Could not get SMA for [%s]. %s" % (vsymb, e), 'red'))
        return 0.0



def alpaca_get_ticker_price(vsymb):
    # Get last price of a ticker.
    return float(vapi.polygon.last_quote(vsymb).askprice)


if __name__ == "__main__":
    try:
        import sys

        #print(ind_moving_average("AAPL", 30))
        #sys.exit()

        vres = alpaca_get_ticker_price("AAPL")
        print(vres)
        sys.exit()

        vres = alpaca_get_ticker_price("WRN")
        print(vres)
        sys.exit()

        # 1Min 5Min 15Min 1D
        vbars = vapi.get_barset("INPX", timeframe="1D", limit=200)
        vbars = vbars['INPX']
        week_open = vbars[0].o
        week_close = vbars[-1].c
        percent_change = (week_close - week_open) / week_open * 100

        print(week_open)
        print(week_close)
        print(percent_change)

        sys.exit()
        vbuy_price = float(vapi.polygon.last_quote('SENS').askprice)

        for vticker in VTICKERS:
            print(ind_moving_average(vticker['Symbol'], 50))
            print(ind_moving_average(vticker['Symbol'], 200))
            print("\n")
        """
        print(ind_moving_average('SHIP', 200))
        """

    except KeyboardInterrupt as e:
        print("[* stocks_broker] Exit broker debugger.")
        sys.exit()