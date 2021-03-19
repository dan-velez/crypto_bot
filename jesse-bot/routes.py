# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Make sure to read the docs about routes if you haven't already:
# https://docs.jesse.trade/docs/routes.html
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from jesse.utils import anchor_timeframe

vstrategy = 'TestStrategy'

# trading routes
routes = [
    # ('Binance', 'BTCUSDT', '1m', vstrategy),
    # ('Binance', 'PROS/ETH', '1m', vstrategy)
    ('Binance', 'CHZBNB', '1m', vstrategy)
]

# in case your strategy requires extra candles, timeframes, ...
extra_candles = [
    # ('Binance', 'BTCUSDT', anchor_timeframe('4h')),
]
