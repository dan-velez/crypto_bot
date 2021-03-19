# stocks_get.py - Get all penny stocks for the day.

from selenium import webdriver
from bs4 import BeautifulSoup
import json

VTICKERS_FILE = ".\\data\\tickers.json"

vres = []

def mw_pstocks():
    "Get updated penny stocks on NASDAQ, NYSE, and AMEX."
    global vres

    for vpage in range(100):
        print("[* stocks_get] Requesting marketwatch.com tickers page: [%s]" % vpage)

        vurl = ("https://www.marketwatch.com/tools/"+
            "stockresearch/screener/results.asp?"+
            "TradesShareEnable=True&TradesShareMax=5&"+ # Max share price is $5
            "PriceDirEnable=False&PriceDir=Up&"+
            "LastYearEnable=False&TradeVolEnable=False&"+
            "BlockEnable=False&PERatioEnable=False&"+
            "MktCapEnable=False&MovAvgEnable=False&"+
            "MovAvgType=Outperform&MovAvgTime=FiftyDay&"+
            "MktIdxEnable=False&MktIdxType=Outperform&"+
            "Exchange=All&IndustryEnable=False&Industry=Accounting"+ # All exchanges
            "&Symbol=True&CompanyName=True&Price=True&Change=True&"+
            "ChangePct=True&Volume=True&LastTradeTime=False&"+
            "FiftyTwoWeekHigh=False&FiftyTwoWeekLow=False&PERatio=False&"+
            "MarketCap=False&MoreInfo=False&SortyBy=Price&"+
            "SortDirection=Ascending&ResultsPerPage=OneHundred&"+
            "PagingIndex=%s" %(vpage*100))

        # print("[* stocks_get] Request URL: " + vurl)

        # Request the rendered webpage.
        chromedriver = ".\\bin\\chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('log-level=3')
        browser = webdriver.Chrome(executable_path=chromedriver, 
                                chrome_options=options)
        browser.get(vurl)

        # Parse and append to memory.
        print("[* stocks_get] Response size: %s bytes" % len(browser.page_source))
        vsoup = BeautifulSoup(browser.page_source, 'lxml')
        # open(".\\data\\stocks.html", "w+").write(str(vsoup))

        try:
            vtable = vsoup.find('table')
            table_data = [[cell.text for cell in row("td")]
                         for row in vsoup("tr")]
            
            if len(table_data) == 0: break

            for vrow in table_data:
                if len(vrow) < 1: continue
                vrow_json = {
                    "Symbol": vrow[0],
                    "Company Name": vrow[1],
                    "Price": vrow[2],
                    "Change": vrow[3],
                    "Change %": vrow[4],
                    "Volume": vrow[5]
                }
                vres.append(vrow_json)
            
            print("[* stocks_get] Total rows: [%s]" % len(vres))
        except Exception as e:
            print("[* stocks_get] No table exists! Stop scraping. [%s]" % e) 
            break
    
    # Write the current tickers to disk
    write_tickers()


def write_tickers():
    # Parse change % column to float.
    print("[* stocks_get] Writing tickers to disk...")
    for vrow in vres:
        vval = vrow['Change %'].split('%')[0]
        if vval.startswith('+'): vval = vval[1:]
        vrow['Change %'] = float(vval)
        vrow['Price'] = float(vrow['Price'])
        vrow['Change'] = float(vrow['Change'])

    # Write results to disk.
    open(VTICKERS_FILE, "w+").write(json.dumps(vres, indent=4))
    print("[* stocks_get] Wrote [%s] rows to: [%s]\n" % (
        len(vres), VTICKERS_FILE))

    return vres


def filter_pstocks():
    # Filter according to rules.

    print("[* stocks_get] Filtering stocks...")

    vtickers = json.loads(open(VTICKERS_FILE, "r").read())
    vprice = 1.00    # Highest price threshold.
    vchange = -100   # Lowest change percentage.

    vfiltered = []

    for vrow in vtickers:
        if (vrow['Change %'] > vchange and 
            vrow['Price'] <= vprice and 
            (not 'Rt' in vrow['Company Name']) and
            (not 'Wt' in vrow['Company Name'])):

            vfiltered.append(vrow)

    open(VTICKERS_FILE, "w+").write(json.dumps(vfiltered, indent=4))

    print("[* stocks_get] Filterd [%s] tickers." % len(vfiltered) )
    return vfiltered


if __name__ == "__main__":
    print("== Scrape MarketWatch.com "+"="*64) # 1272

    try:
        vstocks = mw_pstocks()
        # print("")
        # print(vstocks)

        vstocks_filtered = filter_pstocks()
        # print(vstocks_filtered)

    except KeyboardInterrupt as e:
        print("[* stocks_get] Exit scraper...")
        write_tickers()
        filter_pstocks()