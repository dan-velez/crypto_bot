import pandas as pd
import json
from termcolor import colored
import alphavantage
print(alphavantage)
VPSTOCKS_FILE = '.\\data\\pstocks.json'


def pstocks_sorted():
    # List the penny stocks listed by price.
    VPSTOCKS = pd.read_csv(VPSTOCKS_FILE)
    
    for i,vrow in VPSTOCKS.iterrows():
        # print("%s: %s" % (vrow["Symbol"], colored(vrow["Price"], "green")))
        print("%s: %s" % (colored(vrow["Company Name"], "yellow"), colored(vrow["Price"], "green")))

# pstocks_sorted()


def dict_test():
    vstocks = json.loads(open(VPSTOCKS_FILE, "r").read())
    for vrow in vstocks:
        # change_val(vrow)
        if vrow["Symbol"] == "ROYT":
            vstocks.remove(vrow)
    open(".\\data\\test.json", "w+").write(json.dumps(vstocks, indent=4))


def change_val(vrow):
    vrow["price"] = 100.50
    open(VPSTOCKS_FILE, "w").write()


def test_gains_file():
    # Gains History
    VGAINS_FILE = '.\\data\\gains.csv'
    VGAINS = pd.read_csv(VGAINS_FILE)
    VGAINS = VGAINS.drop(columns=["Unnamed: 0"])

    vtotal_gain = 0.0

    for i,vrow in VGAINS.iterrows(): 
        vcurrent = float(vrow["sell_price"])
        vlast_price = float(vrow["buy_price"])
        vchange = ((float(vcurrent)-vlast_price)/vlast_price)*100
        print(vchange)

        VGAINS.at[i, 'gain %'] = vchange

        vtotal_gain += vchange
        VGAINS.to_csv(VGAINS_FILE)

    print(VGAINS)
    print(vtotal_gain)


def test_change_function():
    vstart_price = 5
    vcurrent = 8
    vres = round((100 / vstart_price) * (vcurrent - vstart_price))
    print(vres)