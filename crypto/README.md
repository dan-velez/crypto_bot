# crypto-bot #
Bot created using CCXT lib, runs automations for creating, 
testing, and live running cryoto trading strategies.


## notes ##
* 24/7 market
* No PDT
    * Can trade consistently with as little amount of money
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


## todo ##
* write algo using just data file.
    * Complete custom bot using custom data format and API

* `crypto-bot` -> imports all files into **1 bot program**.
* Use `argparse` library to design program interface. (TAOUP)


## exchanges ##
* Some frameworks / bots only work with certain exchanges.
* Certain exchanges have certain coins.
* Not all exchanges have all coins.
* Choose exchange + framework + coins.


## blockchain ##
* Records of transactions connected via link.
* One block attached to another
* CC blockchains are transparent, anyone can access records
* Cryptographics links
* Any discepency is quickly detected


## mining ##
* when transactions are verified
* when new blocks are added to the chain
* mining computer select transaactions from a pool
* check if sender has enough funds
* check if sender authorized
* miners have computers that solve algorithms to store blocks.
* miners earn block rewards that deposit into bank accounts.


## jesse ##
* trading framework made for python
* Supported exchanges:
    Binance
    Testnet Binance Futures
    Binance Futures
    Bitfinex
    Coinbase
* generate one jesse bot, add strategies


## positions ##
* short means to sell
* long means to buy


## market making bots ##
* place several buy and sell orders to net in a quick profit.
* implements several indicators and trading strategies.


## adding wallet to broker ##
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
1. Open wallet
2. Connect bank account
3. Sign up for exchange
4. Place order for currency
