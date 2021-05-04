# crypto-bot #
**crypto-bot** is a swiss army knife for crypto trading. It is
used to probe coin and exchange data, download historical 
market data and backtest strategies on this data. It will
also be able to live test these strategies using a real crypto
wallet.


## installation ##
Requires `python >= 3.6`. Installation involves cloning the repo to your local
disk, then running the `setup.py` script.
```
$ git clone https://github.com/dan-velez/crypto_bot
$ cd crypto_bot
$ python setup.py install
```
This will expose the command `crypto_bot.exe` to your terminal.


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


# Download historical data for backtesting. 
crypto-bot history --exchange "coinbasepro" --symbol "BTC/USD" --start 20210101 --end 20210501 --timeframe '1m'
```

## paper broker ##
The paper broker will mimic a wallet/exchange/bank that is used to store your
assets. It is a JSON file that is saved to the disk and is in the following
format:
```json
{
    "total": 0,
    "assets": [
        {
            "exchange": "coinbasepro",
            "pair": "USD/MOCK",
            "buy_price": 0.005,
            "buy_date": "20210501:01:00"
        }
    ],

    "trades": [
        {
            "exchange": "coinbasepro",
            "pair": "USD/MOCK",
            "buy_price": 0.004,
            "buy_date": "20210501:01:00",
            "sell_price": 0.006,
            "sell_date": "20210501:02:00",
            "profit_loss": 50.00
        }
    ]
}
```


## bot woorkflow ##
* use the bot to  select assets with the `exchange` command
    * print out to assets list

* paper portfolio to test out strtegies and not lose any real money

* create strategies using statistical indicators

* use `run` command to test the strategy on a live market data feed


## TODO ##
* for command `run`, add strategy and broker class parameters.

* fully implement paper broker and paper portfolio (JSON file on disk).

* for command `exchanges`, add a datestamp to the output pair.

* for command `exchanges`, add fetch only USD pairs

* for command `exchanges`, size parameter is total number of pairs retrieved,
  not total size of the exchange.

* for command `exchanges`, add a flag --no-assets, which will force the bot to
  just return the size attribute of the exchanges, rather than probe the coins.

* For live trading with real wallet, need to determine:
    * how long does a BUY order take to complete? Instant?
    * how long does a SELL order take to complete? Instant?