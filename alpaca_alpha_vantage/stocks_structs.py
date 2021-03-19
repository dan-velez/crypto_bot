# stocks_structs.py - Persistent structures that trader bot will use during runtime.
# TODO: Change file names: portfolio.json, profits.json, tickers.json

import json
from termcolor import colored

# Investments Portfolio
VPORTFOLIO_FILE = ".\\data\\portfolio.json"
# This is the struct of the current BOUGHT stocks for the bot.
# Bot will check these until they are ready to be sold.
VPORTFOLIO = json.loads(open(VPORTFOLIO_FILE, "r+").read())


# Stock Tickers
VTICKERS_FILE = '.\\data\\tickers.json'
VTICKERS = json.loads(open(VTICKERS_FILE, "r+").read())


# Profits History
VGAINS_FILE = '.\\data\\profits.json'
# This shows the gain/loss history of the bots investments.
# Used to calculate the profit at the end of the day.
VGAINS = json.loads(open(VGAINS_FILE, "r+").read())


## Investments Struct  #########################################################

def investments_update_last_price(vname, vprice):
    # Update the last price in investments struct. Save to disk.
    global VPORTFOLIO

    # print("[* stock_mon] Update %s last price to %s" % (vname, vprice))

    for vrow_inv in VPORTFOLIO:
        if vrow_inv["symbol"] == vname:
            vrow_inv['last_price'] = vprice
            open(VPORTFOLIO_FILE, "w").write(json.dumps(VPORTFOLIO, indent=4))
            return


def has_investment(vname):
    # Check investments for a particular stock.
    for vrow_inv in VPORTFOLIO:
        if vrow_inv["symbol"] == vname:
            return True
    return False


def remove_investment(vname):
    # Remove investment from in memory and disk struct.
    global VPORTFOLIO
    
    for vrow_inv in VPORTFOLIO:
        if vrow_inv["symbol"] == vname:
            VPORTFOLIO.remove(vrow_inv)
            open(VPORTFOLIO_FILE, "w").write(json.dumps(VPORTFOLIO, indent=4))
            break


def add_investment(vname, vstart_price, vbuy_price, vshares, vlast_price):
    # Add investment to in memory and disk struct.
    global VPORTFOLIO
    
    VPORTFOLIO.append({
        "symbol": vname, 
        "start_price": vstart_price, 
        "buy_price": vbuy_price, 
        "shares": vshares,
        "last_price": vlast_price
    })
    open(VPORTFOLIO_FILE, "w").write(json.dumps(VPORTFOLIO, indent=4))


def get_investment(vname):
    # Retrieve info on the investment and return.
    
    for vrow in VPORTFOLIO:
        if vrow["symbol"] == vname:
            return {
                "symbol": vrow["symbol"],
                "start_price": vrow["start_price"],
                "buy_price": vrow["buy_price"],
                "shares": vrow["shares"],
                "last_price": vrow["last_price"]
            }
    return None


def get_pstock(vname):
    # Return the stock row from penny stocks file..

    for vrow in VTICKERS:
        if vrow["Symbol"] == vname:
            return {
                "Symbol": vrow["Symbol"],
                "Company Name": vrow["Company Name"],
                "Price": vrow["Price"],
                "Change": vrow["Change"],
                "Change %": vrow["Change %"],
                "Volume": vrow["Volume"]
            }
    return None


if __name__ == "__main__":
    print("[* stocks_structs] Number of tickers being checked: [%s]" % len(VTICKERS))
    print("[* stocks_structs] Portfolio size: [%s]" % len(VPORTFOLIO))