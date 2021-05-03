#!/usr/bin/python


class CryptoStrategy:
    """Default strategy class for using the LiveFeed and Backtest objects.
    Inherit these functions to create custom strategies. This is just a default
    strategy for demo purposes."""

    def should_open (self,vbar, vhist):
        """If the position is closed, determine if we should BUY."""
        # Open if:
        #     change_percent from day_open > 5.
        #     not currently open.
        #     has enough volume to perform trade.
        vchange = vbar['close'] - vhist['initial']
        vchange_percent = round(
                (vchange / vhist['initial']) * 100, 2)

        # Print debug info.
        if vchange_percent > 0: vcolor = 'green'
        else: vcolor = 'red'
        print(colored(
            "[* crypto_backtest] change since open: %s%%" % 
            vchange_percent, vcolor))
        print('')
        return False

    def should_close (self, vsymb, vhist):
        """If the position is open, determine if we should SELL."""
        # Close if:
        #   change_percent since buy price < -5
        #   Take 5% loss
        #   OR if change % > 5
        #   Take 5% profit
        return False