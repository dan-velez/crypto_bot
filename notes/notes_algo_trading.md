# Algo Trading Notes #

* Mix of finance and programming
* Quantopian trading contests
* **Stick to consistent strategy**
* Accept losses, **do not change risk parameters**
* Use **stock scanners** to add symbols to searchable stocks
* **Moving average convergence divergence**
* **Understand** how to use SMA to make trades and profits
  * Using Alpaca and backtrader API
  * Move on to more complex strategies from here

* **try to implement strategy+ with backtrader**
* **blueshift has documentation and courses**


## ML ##
* Gather large amounts of intraday minute data
* Label all data where good trades would be
* Make prediction based on point in line


## TODO ##
* Create IEX data harvester
  * Need to gather the data to be backtested on.
  * Gather data daily, from different symbols
  * Keep in one directory.
  * Create script that gathers this data.
  * Feed into runner.. needs to have same date, or read the date.

* Create configurable runner
  * Add parameters to script


## Workflow Example ##
```bash
# Get intraday minute data for a symbol. Save to directory.
get_iex_hist_data.py NAKD 0310 historical/

# > edit strategy class <

# Run backtesting on data
runner.py strat_sma.py backtest historical/NAKED_0310.csv

# Run on list of tickers
runner.py strat_sma.py backtest list historical/NAKED_0310.csv

# Live test
runner.py strat_sma.py live tickers_file.json
```


## Input ## 
* Bot will require three inputs:
  * Stocks filter
    * **stock_pennies.py**
    * Also change stocks filter in stock_monitor main loop!

  * Buy pattern
  * Sell pattern
  * Invest amount
  * Check interval


## Data Folder ##
* **investing.csv**

* **pstocks.csv**
  * The stocks list that the bot will check throughout the day.
  * ,Symbol,Company Name,Price,Change,Change %,Volume
  * 0,LMFAW,LM Funding America Inc. Wt,0.0022,-0.0011,-33.33,9800 

* **gains.csv**

* **resp.csv**

* **Sym_*.csv**


## Source Files ##

### Main ###
* **stock_monitor.py**
  * Run infinite loop through `pstocks.csv` and `investing.csv`.
  * Use Alpaca API to probe for current price of stock.

* **stock_pennies.py**
  * Retrieve stocks list from online. Save to `pstocks.csv`.
  * Check `https://www.marketwatch.com/tools/stockresearch/screener/` for filter options.

* **stock_alert.py**
  * Send an email alert to stocks bot email account.  

### Utils ###
* **stock_hist.py**
  * Used to get the history of a stock to try and make a prediction w/ ML.

* **stock_invest.py**
  * Show gain/loss from investments file. Automated report.


## Notes ##
* Follow algo with one symb, see how it acts
* tries to get all the small gains from one symb throughout day
* peak with slope m
  calc peak
  sell when change -5% (might sell alot, continually lose 5%)
  sell peak again

* 15-20% spikes happen within 5 minutes
* Or lower change alert threshold
* Need to calculate slope at different points, determine at what points
  the stock will continue to rise. when is it being pumped.
* In 5 min, TLGT spiked from 15-35%
* Detecting the 15% change, you are detecting after the spike.. detect at 5-7
    * How many stocks at 7% rise to 15%?
        * Examine hist
* How quickly spikes rise, tell by lookinh at graphs (slope)
* How to detect spikes in plot chart
* Distinguish up from buy price, up from start prie



## Test API Code ##
```python
def api_example():
    vapi = tradeapi.REST(CALPACA_KEY, CALPACA_SKEY)
    """
    vsymbol = vapi.get_asset('INPX')
    print(vsymbol)

    vsymbol = vapi.get_asset('GOOG')
    print(vsymbol)

    vsymbol = vapi.polygon.historic_agg_v2('INPX', 1, 'day', _from='2019-12-17', to='2019-12-18').df
    print(vsymbol)

    print("*"*80)
    vsymbol = vapi.polygon.historic_trades_v2('INPX', '2019-12-17').df
    print(vsymbol)
    #vsymbol.to_csv('resp.csv')
    """
    print("*"*80)
    vsymbol = vapi.polygon.last_quote('INPX').askprice
    print(help(vsymbol))
    print(vsymbol.askprice)
```


## Trading/Finance ##
* Supply / Demand
* Asset Types (stocks, options, futures, forex)
* Buying vs Selling
* Bid/Ask Spreads
* Liquidity
* Trading on Margin
* Risk Management
* Order Types 


## Trading Strategies ##
* HF trading is not for retail traders (very expensive to develop and use)
* Check moving average
* When it hits, it might go up...
* Use 50 day MA and 200 day MA
* High freq. trading - Make a lot of small gains
* Arbitrage trading
  * Trading between markets
* Trend-following strategies
  * Trade based on highly technical indicators

* Market cycles - Need to continually develop new algorithms
  * Essentially programming in a trader's pychology

* **Example** (not recommended to use):
  * BUY If ABC crosses above 30-day MA
  * SELL If ABC crosses below 30-day MA


## Development Strategy ##
1. Find an inefficiancy in the market to exploit
2. Transalte into code
3. Backtest on historical data (backtest on weekends)
4. Optimize (continuous)
5. Add safeguards (stop losses, exposure limits, i.e risk mgmt)
6. Optimize and test
7. Paper trading
8. Use live account (start with small money)
9. Scale up (give the algo more capital to trade with)
10. Optimize and monitor (especially in beginning)


## References ##
* https://algotrading101.com/learn/alpaca-trading-api-guide/
* https://algotrading101.com/learn/backtrader-for-backtesting/
* https://www.investopedia.com/articles/active-trading/090415/only-take-trade-if-it-passes-5step-test.asp
* https://algotrading101.com/learn/quantitative-trading-strategies/
* https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html < Auth variables should be secure
* https://www.alphavantage.co/documentation/#technical-indicators
* https://alpacablog.squarespace.com/blog/2018/7/24/building-a-simple-stock-trading-bot-by-using-brokerapi
* https://alpaca.markets/docs/api-documentation/api-v2/market-data/bars/ 
* https://alpaca.markets/docs/alpaca-works-with/blueshift/
* https://mrjbq7.github.io/ta-lib/ **TA-Lib Indicator Functions**
* https://alpaca.markets/docs/api-documentation/how-to/market-data/