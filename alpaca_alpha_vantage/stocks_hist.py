# stock_hist.py - Get stock ticker data.

from io import StringIO
import pandas as pd
import requests
import json
import csv
import time


CAPIKEY = "SPFB2UXLAGUCP0NP"
CAPIEP  = "https://www.alphavantage.co/query"


def alpha_vantage(vreq, vsymbol):
    "Make a request to alpha vantage api, return CSV."
    
    try: vresp = requests.get(vreq)
    except Exception as e:
        print("[* stock_hist] Could not request alpha-vantage. %s" % e)
        return pd.DataFrame()
    print("[* stock_hist] Request %s: %s" % (vsymbol, vresp.status_code))

    # Parse response.
    try: df = pd.read_csv(StringIO(vresp.text), 
         sep=',', parse_dates=True)
    except Exception as e:
        print("[* stock_hist] Could not parse csv response: %s; %s" % 
               (e, vresp.text))
        return pd.DataFrame()

    return df


def get_list_symbols(vmarket="NYSE"):
    "Reteive a list of ticker symbols to choose to trade from."
    
    # Should try to manually,stragegically select these.
    vpath = ".\\data\\Sym_%s.csv" % vmarket
    return pd.read_csv(vpath)


def get_ticker_latest(vsymbol):
    "Get the latest price for a symbol."
    
    vreq = (CAPIEP+"?function=GLOBAL_QUOTE"+
           "&datatype=csv"+
           "&symbol=%s&apikey=%s" % (vsymbol, CAPIKEY))
    return alpha_vantage(vreq, vsymbol)


def get_ticker_hist(vsymbol, vsize="full"):
    "Return the ticker values per day or years."

    vreq = (CAPIEP+"?function=TIME_SERIES_DAILY"+
           ("&outputsize=%s&datatype=csv" % (vsize))+
           "&symbol=%s&apikey=%s" % (vsymbol, CAPIKEY))
    #print("[* stock_hist] %s" % vreq)
    return alpha_vantage(vreq, vsymbol)


if __name__ == "__main__":
    "Get ticker data and make a prediction."
    import sys

    print("== RH_Stock_Tool "+"="*32)
    print(get_ticker_latest("INPX"))

    sys.exit()
    if len(sys.argv) < 2:
        print("[*] Usage: python stock_hist <symbol>")
        sys.exit()
    vsymbol = sys.argv[1]
    vtickers = get_ticker_latest(vsymbol)
    vtickers.to_csv('.\\data\\resp.csv')
    for i,vrow in vtickers.iterrows():
        print('%s\n' % vrow)