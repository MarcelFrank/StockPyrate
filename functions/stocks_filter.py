def apply(stocks, custom_filter):

    stocks_filtered = stocks

    # Append whitelisted stocks
    stocks_whitelist_by_stock = []
    if custom_filter["whitelist_stocks"]:
        [stocks_whitelist_by_stock.append(stocks_filtered[[stock_tuple[0] for position, stock_tuple in enumerate(stocks_filtered)].index(stock)]) #1
        for stock in custom_filter["whitelist_stocks"]
        if stock in [stock_tuple[0] for position, stock_tuple in enumerate(stocks_filtered)]] #1
    
    # Append whitelisted indices
    stocks_whitelist_by_index = []
    if custom_filter["whitelist_indices"]:
            [stocks_whitelist_by_index.append(stock)
            for index in custom_filter["whitelist_indices"]
            for stock in [stock_tuple for position, stock_tuple in enumerate(stocks_filtered)]
            if index == stock[3]]

    # Append whitelisted sectors
    stocks_whitelist_by_sector = []
    if custom_filter["whitelist_sectors"]:
            [stocks_whitelist_by_sector.append(stock)
            for sector in custom_filter["whitelist_sectors"]
            for stock in [stock_tuple for position, stock_tuple in enumerate(stocks_filtered)]
            if any([sector.upper() in stock[2].upper()])]
       
    # Join whitelists and erase duplicates
    if custom_filter["whitelist_indices"] or custom_filter["whitelist_stocks"] or custom_filter["whitelist_sectors"]:
        stocks_filtered = list(set(stocks_whitelist_by_index + stocks_whitelist_by_stock + stocks_whitelist_by_sector))
    
    # Identify stocks listed as components of blacklisted indices
    stocks_blacklist_by_index = []
    [stocks_blacklist_by_index.append(stock[0]) #1
    for index in custom_filter["blacklist_indices"]
    for stock in [stock_tuple for position, stock_tuple in enumerate(stocks_filtered)]
    if index == stock[3]]

    # Join blacklists and erase duplicates
    custom_filter["blacklist_stocks"] = list(set(custom_filter["blacklist_stocks"] + stocks_blacklist_by_index))

    # Delete blacklisted stocks  
    [stocks_filtered.pop([stock_tuple[0] for stock_tuple in stocks_filtered].index(stock)) #1
    for stock in custom_filter["blacklist_stocks"]
    if stock in [stock_tuple[0] for position, stock_tuple in enumerate(stocks_filtered)]] #1

    # Sort stock list alphabetically by stock name
    stocks_filtered = sorted(stocks_filtered)

    return stocks_filtered