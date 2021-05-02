# crypto_coins.py - Implement functions used in the `coins`
# subcommand.

def get_coins (vexchange, vmin_price, vmax_price, vmin_change):
    # Get tickers which fall in a certain price range.
    # Retrieve all symbols as open price.
    # Save to designated JSON path.

    # Fetch symbols from exchange.
    exchange = getattr(ccxt, vexchange)()
    exchange.load_markets()

    # No symbols found.
    if len(exchange.symbols) == 0:
        print("[* tickers] No tickers found on"+
                " exchange %s." % sys.argv[1])
        sys.exit()

    print("[* tickers] found %s symbols." 
            % len(exchange.symbols))

    # Filter symbols by close price < $0.50
    vres = []
    for vsymb_text in exchange.symbols:
        try:
            vbars = exchange.fetch_ohlcv(vsymb_text)
        except Exception as e:
            print("[* crypto_get_tickers] Cannot fetch %s : %s" 
                    % (vsymb_text, e))
            continue

        print('[* crypto_get_tickers] Fetched symbol %s' 
                % vsymb_text)
        print("[* crypto_get_tickers] Num bars for %s: %s" 
                % (vsymb_text, len(vbars)))
        print()

        vdate = pd.to_datetime(vbars[0][0], unit='ms')
        vclose = vbars[-1][-2]
        # TODO: Get 24 hour change %.
        if vclose < 0.50: # && vchange % > 5
            vres.append({
                'symbol': vsymb_text,
                'timestamp': str(vdate),
                'close': vclose,
                'volume': vbars[-1][-1]
            })

    # Write out results.
    print("[* crypto_get_tickers] %s tickers downloaded." 
            % len(vres))
    vfname = "./data/tickers_%s.json" % vexchange
    open(vfname, 'w+').write(json.dumps(vres, indent=4))
