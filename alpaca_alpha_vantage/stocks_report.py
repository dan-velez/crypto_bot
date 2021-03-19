# stocks_report.py - Get updates on your investments.

# import stock_hist as stockh
from stocks_structs import *

CPORTFOLIO = ".\\data\\portfolio.csv"

def old_report():
    df = pd.read_csv(CPORTFOLIO)

    vres = ""
    vinvested = 0
    vearned = 0

    for i,vrow in df.iterrows():
        vsymb = vrow['symbol']
        vprice = vrow['price']

        vhist = stockh.get_ticker_latest(vsymb)
        vopen = vhist.iloc[0]['price'] # Get current price

        # Calc change percentage.
        vchange = round(((100 / vprice) * vopen) - 100)

        # Calculate earned
        vearned += (vprice / 100) * vchange
        if vchange > 0: vchange = "UP %s%%" % vchange
        elif vchange < 0: vchange = "DOWN %s%%" % vchange
        else: vchange = "NO CHANGE"
        vres += '[* stock_invest] %s\t%s\n' % (vsymb, vchange)

        # Accum invested amount.
        vinvested += vrow['price'] * vrow['shares']
    
    # Calc total invested
    print("\n%s\n" % vres)
    print("[* stock_invest] Total invested: %s" % (vinvested))
    print("[* stock_invest] Gain/Loss: %s" % (vearned))
    # TODO: Show percentage gain/loss


def report_main():
    vtotal_bought = 0
    vtotal_sold = 0
    vtotal_trades = 0
    
    vtotal_portf = 0
    vtotal_in_portf = 0

    for vprofit in VGAINS:
        if not 'time' in vprofit.keys(): continue
        if '2020-06-18' in vprofit['time']:
            vtotal_bought += vprofit['buy_price']
            vtotal_sold += vprofit['sell_price']
            vtotal_trades += 1

    for vinv in VPORTFOLIO:
        vtotal_in_portf += 1
        vtotal_portf += vinv['buy_price']

    print("Total Profit: $%s" % round(vtotal_sold - vtotal_bought, 2))
    print("Total Bought: $%s" % round(vtotal_bought, 2))
    print("Total Sold:   $%s" % round(vtotal_sold, 2))
    print("Total Trades:  %s" % vtotal_trades)
    print("")
    print("Total Left in Portfolio:  %s" % vtotal_in_portf)
    print("Total Portfolio Worth:   $%s" % round(vtotal_portf, 2))
    print("")

if __name__ == "__main__":
    print("== Trader Bot Report "+"="*32+"\n")
    report_main()