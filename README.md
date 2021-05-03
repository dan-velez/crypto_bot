# crypto-bot #
**crypto-bot** is a swiss army knife for crypto trading. It is
used to probe coin and exchange data, download historical 
market data and backtest strategies on this data. It will
also be able to live test these strategies using a real crypto
wallet.

## installation ##
* Install `Python 3.6` (not tested on any other Python versions).
* Install requirements file with 
  `pip install -r requirements.txt`


## settings ##
The file `.crypto.json` cotains some configuration for the bot.
This file is sensitive and specific to each trader. This should
be created manually. It should contain the following keys:

* `wallet` - Set to `paper` or `coinbase`.
* Coinbase wallet settings:
  * `cb-secret` - Coinbase API secret.
  * `cb-apikey` - Coinbase API Key.
  * `cb-passphrase` - Coinbase API passphrase.`


## usage ##
**crypto-bot** contains several commands for automating 
crypto trading tasks: (not all have been implemented)

### exchanges ###
> View and download exchange data such as size and which 
  coins it contains. Use this command to generate a list 
  of coins / exchange pairs to run strategy on. 

### coins ###
> View and download data on coin / exchange pair such as
  OHLCV for a coin. Use this command to download historical 
  data to run backtests on.

### backtest ###
> Run a strategy on a historical data file. The history data
  file should be generated using the `history` subcommand. The
  strategy file is a python source file which contains your
  entry and exit function `should_buy()` and `should_sell()`.

### broker ###
> Functions that interact with your wallet and portfolio.
  Initiate buy / sell for a coin or view portfolio data. The default broker is 
  a paper broker which uses the file `paper_portfolio.json` to store its 
  assets. The paper broker is used to test strategies and will not use any real
  money.

### run ###
> Run a strategy on a live feed. Select your strategy source
  file. The wallet set in the settings file will be used.

### help message ###
```
usage: crypto-bot [-h] {exchanges,coins,backtest} ...

Retrieve crypto data and run back tests, live tests, and live trading.     

positional arguments:
  {exchanges,coins,backtest}
                        Command
    exchanges           View / download information on available exchanges.
    coins               View / download OHLCV data on coins of an exchange.
    backtest            Backtest a strategy on historical data.

optional arguments:
  -h, --help            show this help message and exit

crypto-bot <command> -h displays help on a particular command.
```


## examples ##
```bash
# Get a list of all exchanges and all coins available in each.
# Should print the latest bar for each coin.
crypto-bot exchanges
crypto-bot exchanges --outfile exchanges.json


# Get exchange size and coins available for certain exchanges. 
crypto-bot exchanges --list "coinbase, kraken" --outfile coinbase_kraken.json


# Get exchanges that only contain less than 50 assets available.
crypt-bot exchanges --size-limit 50 --outfile small_exchanges.json

# Run live ticker feed with a list of assets generated from exchanges command.
crypto-bot run --assets .\data\coins_coinbasepro.json
```


## TODO ##
* Add `run` command to bot. Params:
  * asset file
  * strategy class

* fully implement paper broker and paper portfolio (JSON file on disk).

* for command `exchanges`, add a flag --no-assets, which will force the bot to
  just return the size attribute of the exchanges, rather than probe the coins.

* for command `exchanges`, fetch only USD pairs

* for command `exchanges`, size parameter is total number of pairs retrieved,
  not total size of the exchange.

* For live trading with real wallet, need to determine:
  * how long does a BUY order take to complete? Instant?
  * how long does a SELL order take to complete? Instant?