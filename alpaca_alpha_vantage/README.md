# Stock Tool

## TODO
    * Make invest_check.py script
    * Test penny stocks predictions


## Process
    * Get training data from API
        * Adjust parameters.
    * Bot to get data with specific parameters (simple, manual pred.).
    * Build prediction model from there.

    * Split into training and test data
    * Train model, using custom ANN
    * Test predictions, tune trainer

    * Make local database of all stock tickers (fast access)


## Categorial NN:
    * Will increase by n in one day
    * Use all values over 5 years of all stocks,
    * Use moving average variables and S&P 500 values.
    * Training row: 30 days(O,C,L,H), MAs, MISC,
    * Training row: 10X of (+/-) at EOD


## Ideas
    * Train a model for a particular symbol, all time
    * Train a model on all symbols, all time
    * Download ALL data, train for different snaphots.
    * "My opinion is that combining sentiment analyses with deep learning models to predict the price based on historical data would yield great results."

## Types
    * Try high frequenct trading model
    * Try day trading model
    * Must train 1 model per ticker. Training must be done within a day.


## Notes
    * Try training according to categories:
        * What is a good trade?
        * What does a promising time series look like?

    * Different variable to try to get the most accurate prediction:
        * Day range per ticker
        * Activation function

    * Your performance trend should mimic that of the overall market.
    * "The bot tracks specific patterns, such as what usually 
       happens at X hour and decides to place a trade when the 
       predicted profit rate is greater than a certain threshold."

    * Blue chip stocks are easier to predict than penny stocks.

    * Identify "Pump and Dump" penny stocks
    * Market trends, reliable patterns that can be used to trade succssfully
    * Assets and revenue of a company

    * Train to classify stocks will + by >49% next day
        * Find penny stocks current, and historical with +49%
        * Store x data prior in DB
        * Collect large amounts of these

## Stocks bot
    * ragingbull.com
    * History of stock market

## Lookup:
    * DEX trading software
    * Raging Bull
    * History of Stock Market

## Performance
SNNA 30   0.146
GHSI 
CFRX 
OCGN 10  0.415
INPX 100 0.0382

* Save investment history, track amount gained/lossed

* During the day may be a better indicator, tell when slope of regression becomes steep for some points

* (Analytics) Create script: Which stocks were pumped during previous day
    * Inidcated by change %

* Need to take right data at right times: Look for almost peek
    * DL penny stocks at start
    * Every 30 min, request a select number of stock prices / intraday hist
    * Look for pre-spike
    * Buy
    * Every 30 min, request on your investmeds
    * Look for pre-plummet
    * Sell
    * Wait till next day

* Night before may indicate pre-spike as well

* search_buy_loop():
    marketwatch
    search all pstocks
    compare to old pstocks file, if present
    track change from start of day
    * Marketwatch needs to be realtime
    
* Need strategy when stock invested goes negative:
    * Never let yourself lose more than X dollars on a stock


# Results

## 12-2019
    SNNA -  Reached high of 58% @ 9.30 am
        * Had a low price, and high change% EOD
        * High volume +1mil

    INPX - stayed relativley the same. Kept.

    CFRX - Reached high of 30% @ 9.50am, sold at 25%
        * Had a low price, and high change% EOD
        * High volume +1mil

# If stock is not improving, leave until pumped. Might be days, weeks
# Plumetted, but still a +change from original stock opening
# EOD, look at pattern for pump and dump... what hour did they peak?
# Check 52-week high, volume, price, change


# Functions:
    * Find stocks (work hours)
    * Find stocks (after hours)
    * Tell when to sell
    * Update inv. status

## Strategy
    * Range of loss / gain example (with loss threshold):
    ** never lose more than 15% of inv. Perfect algo to minimize loss range.
        -50 - 400
        * BEST CASE (400):
            * $300 - SYM1 ^ 60
            * $125 - SYM2 ^ 25
            * $100 - SYM3 ^ 1

        * WORST CASE (-50):
            * $300 - SYM1 v 5
            * $125 - SYM2 v 5
            * $100 - SYM3 v 5


## Scripts
    * stock_monitor - Use pstocks.csv and investing.csv to monitor stocks for buy/sell points.
    * stock_perf.py - show graph of symb.. maybe more eff to open browser and pull up stock... send link in email
    * stock_order.py - place buy and sell orders
    * stock_invest.py - Show full stats of current investmetn: bought at, current price/change, sold at price/change