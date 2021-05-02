# crypto-bot #
**crypto-bot** is a swiss army knife for crypto trading. It is
used to probe coin and exchange data, download historical 
market data and backtest strategies on this data. It will
also be able to live test these strategies using a real crypto
wallet.

## installation ##
* Install `Python 3.6`
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
  coins it contains.

### coins ###
> View and download data on coin / exchange pair such as
  OHLCV for a coin. 

### history ###
> View and download historical data for a coin / exchange
  pair over a given time frame.

### backtest ###
> Run a strategy on a historical data file. The history data
  file should be generated using the `history` subcommand. The
  strategy file is a python source file which contains your
  entry and exit function `should_buy()` and `should_sell()`.

### broker ###
> Functions that interact with your wallet and portfolio.
  Initiate buy / sell for a coin or view portfolio data.

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
```