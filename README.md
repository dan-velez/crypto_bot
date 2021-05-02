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

* `wallet` - Set to `paper` or `coinbase`/
* Coinbase wallet settings:
  * `cb-secret` - Coinbase API secret.
  * `cb-apikey` - Coinbase API Key.
  * `cb-passphrase` - Coinbase API passphrase.`


## usage ##
**crypto-bot** contains several commands for automating 
crypto trading tasks:

### exchanges ###
> View and download exchange data such as size and which 
  coins it contains.

### history ###
> View and download historical data for a coin / exchange
  pair over a given time frame.

### coins ###
> View and download data on coin / exchange pair such as
  OHLCV for a coin. 

## broker ##
> Functions that interact with your wallet and portfolio.
  Initiate buy / sell for a coin or view portfolio data.

### backtest ###
> Run a strategy on a historical data file. The history data
  file should be generated using the `history` subcommand. The
  strategy file is a python source file which contains your
  entry and exit function `should_buy()` and `should_sell()`.

### run ###
> Run a strategy on a live feed. Select your strategy source
  file. The wallet set in the settings file will be used.


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


## notes ##
The rest of these sections of documentation are notes on
various concepts of crypto trading and finance.

* 1,000s of currencies
* ~125 exchanges on CCXT lib (504 in total)
* Buy/Sell currencies between exchanges
* Need to have a **wallet**
* Crypto currency markets are decentralized
* Run on networked computers
* Bough/Sold via exchanges
* Currencies exist as a digital record on a blockchain
* Exchange between users is done through a wallet
* The transaction must be verified through 'mining'
* New cryptocurrency tokens are created also via 'mining'
* Free from **economical and political concerns**.


### exchanges ###
* Some frameworks / bots only work with certain exchanges.
* Certain exchanges have certain coins.
* Not all exchanges have all coins.
* Choose exchange + framework + coins.


### blockchain ###
* Records of transactions connected via link.
* One block attached to another
* CC blockchains are transparent, anyone can access records
* Cryptographics links
* Any discepency is quickly detected


### mining ###
* when transactions are verified
* when new blocks are added to the chain
* mining computer select transaactions from a pool
* check if sender has enough funds
* check if sender authorized
* miners have computers that solve algorithms to store blocks.
* miners earn block rewards that deposit into bank accounts.


### positions ###
* short means to sell
* long means to buy


### market making bots ###
* place several buy and sell orders to net in a quick profit.
* implements several indicators and trading strategies.


### adding wallet to broker ###
```
# Login to Binance using API Key. Use in broker.
# from variable id
# exchange_id = 'binance'
# exchange_class = getattr(ccxt, exchange_id)
# exchange = exchange_class({
#     'apiKey': 'YOUR_API_KEY',
#     'secret': 'YOUR_SECRET',
#     'timeout': 30000,
#     'enableRateLimit': True,
# })
```


### getting crypto ###
* Need to purchase crypto on an exchange, then send the coin to 
  your crypto wallet address.
* Once you have crypto in wallet, use exchange to convert to USD
* Use exchange and wallet address to transfer funds.
* Trading on exchange requires verification process.

1. Open wallet
2. Connect bank account
3. Sign up for exchange
4. Place order for currency

* convert fiat to base currency -> convert base to alt


### wallets ###
* metamask.io
* coinbase


### exchanges ###
* LOW price HIGH volitility
* crypto / fiat (USD)
* **bitforex**
* **crex24**
* **bittrex**
* **coinbase**
* **etoro**


### trading pairs ###
* assets that can be traded for each other on an exchange.
* some currencies can only be bought with other currencies.
* can be used for arbitrage
* some currencies dont trade crypto/fiat
* **base currency** is the currency u are trading **from**
* often the coin price will be paired with BTC, or how much
  BTC is worth that coin.
* used to compare one coin price to another. Used to esablish
  value.
* To trade XRP to ETH, first find XRP/BTC, then ETH/BTC
* base currency can be BTC, in which all coins can be bought in
* some coins **CANNOT** be bought in fiat.
* Base currency can be BTC, ETH, or LTC