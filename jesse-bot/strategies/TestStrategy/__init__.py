from jesse.strategies import Strategy
from jesse import utils
import jesse.indicators as ta

# Check volume for pumping stocks
# Buy when rising, sell at peak
# Have to guess when asset will rise, peak, and fall

class TestStrategy(Strategy):
    vnum_points = 0

    def should_long(self) -> bool:
        # return true if current candle is a bullish candle
        # print(self.price)
        if self.close > self.open:
            return True
        return False

    def should_short(self) -> bool:
        # return true if current candle is a bearish candle
        self.vnum_points += 1
        if self.close < self.open:
            return True
        return False

    def should_cancel(self) -> bool:
        return True

    def go_long(self):
        # BUY
        # print("BUY")
        qty = 1
        stop_loss_price = self.low - 10
        take_profit_price = self.high + 10
        entry_price = 100

        self.buy = qty, entry_price
        self.stop_loss = qty, stop_loss_price
        self.take_profit = qty, take_profit_price

    def go_short(self):
        # SELL
        # print("SELL")
        qty = 1
        stop_loss_price = self.low - 10
        take_profit_price = self.high + 10
        entry_price = 100

        self.sell = qty, entry_price
        self.stop_loss = qty, stop_loss_price
        self.take_profit = qty, take_profit_price

    def terminate(self):
        print('backtest is done')
        print("%s points on line." % self.vnum_points)
