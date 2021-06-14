def status(key):
    code = {}
    code[111] = "- Parsing stock history..."
    code[112] = "- Parsing dividend history..."
    code[113] = "- Parsing statistics..."
    code[201] = "> Creating stock object:\n"
    code[211] = "- Writing ID...\n"
    code[212] = "- Writing stock symbol...\n"
    code[223] = "- Writing sector information...\n"
    code[213] = "- Writing index information...\n"
    code[214] = "- Writing daily stock prices...\n"
    code[215] = "- Writing weekly stock prices...\n"
    code[216] = "- Writing quartery stock prices...\n"
    code[217] = "- Writing daily transaction volume...\n"
    code[218] = "- Writing dividend history...\n"
    code[219] = "- Writing statistics...\n"
    code[220] = "- Writing daily transaction volume...\n"
    code[221] = "- Writing weekly transaction volume...\n"
    code[222] = "- Writing quarterly transaction volume...\n"
    code[231] = "- Extracting number of total shares (string conversion)...\n"
    code[232] = "! Number of total shares are unknown. Total shares are set to '1'...\n"
    code[233] = "- Extracting number of free float shares (string conversion)...\n"
    code[234] = "- Extracting number of free float shares (string conversion)...\n"
    code[235] = "- Number of free float share is set to same value as total shares...\n"
    code[236] = "! Number of total and free float shares are unknown. Free float shares are set to '1'...\n"
    code[241] = "- Extracting ex date (conversion to datetime object)...\n"
    code[242] = "! Ex date is unknown. Ex date is set to January 01, 1980 (datetime object required)\n"
    code[243] = "- Computing current dividend yield...\n"
    code[244] = "! No dividend is paid. Current dividend yield is set to '0.0001%' (avoid division by zero).\n"
    code[245] = "! Last dividend was paid in last year or later. Current dividend yield is set to '0.0001%' (avoid division by zero).\n"
    code[251] = "- Computing daily transaction amount (shares * daily closing price)...\n"
    code[252] = "- Computing quarterly transaction amount (shares * average price)...\n"
    code[253] = "- Computing transaction amount for the last 12 months (shares * average price)...\n"
    code[258] = "! Number of shares is unknown and market cap is not given in statistics. Market Cap is set to '1'.\n"
    code[259] = "! An error ocurred while trying to compute transaction (prices and dates are out of sync).\n"
    code[261] = "- Computing delta percentage compared to current price...\n"
    code[271] = "- Creating pandas dataframes...\n"
    code[281] = "- Inserting subfolder 'xlsx' (preset in stocks_db.py)...\n"
    code[282] = "- Inserting custom folder as destination for concatenated xlsx files...\n"
    code[291] = "- Writing key facts to be inserted as first sheet in single xlsx files...\n"
    code[301] = "\n> Crawling and parsing of html content of all urls above took (in seconds):\n- "
    code[302] = "> Computing financial data and writing xlsx file took (in seconds):\n- "
    [print(i, end = "") for i in code[key]]

def crawler_task(stock_current):
    print("\n>>>", str(stock_current["name"]).upper(), "is about to be analyzed...")
    
def crawler_get(argument_one, argument_two):
    print("\n> Crawling starts in", argument_one, "seconds:\n- URL:", argument_two)

def crawler_error(code, stock_current, stocks_parsed):
    stocks_parsed["successfully_false"] += 1
    stocks_parsed["successfully_false_names"].append(str(stock_current["name"]))
    code_args_one = {}
    code_args_one[400] = "! Not so successfully parsed stocks up to now::\n- ", stocks_parsed["successfully_false_names"]
    code_args_one[410] = "! Oh no, an error occured while parsing ", str(stock_current["name"]).upper(), "\n- IndexError!\n"
    code_args_one[420] = "! Oh no, an error occured while parsing ", str(stock_current["name"]).upper(), "\n- ZeroDivisionError!\n"
    code_args_one[430] = "! Oh no, an error occured while parsing ", str(stock_current["name"]).upper(), "\n- KeyError!\n"
    code_args_one[440] = "! Oh no, an error occured while parsing ", str(stock_current["name"]).upper(), "\n- ValueError!\n"
    code_args_one[450] = "! Oh no, an error occured while parsing ", str(stock_current["name"]).upper(), "\n- AttributeError!\n"
    [print(i, end = "") for i in code_args_one[code]]
    [print(i, end = "") for i in code_args_one[400]]

def crawler_progression(stocks_filtered, stocks_parsed, average_crawling_delay):
    #if stocks_parsed["successfully"] + stocks_parsed["successfully_false"] != 0:
    if stocks_parsed["successfully"] != 0:
        print("> Successfully parsed stocks up to now:\n-", stocks_parsed["successfully_names"])
    if stocks_parsed["successfully_false"] != 0:
        print("> Not so successfully parsed stocks up to now:\n-", stocks_parsed["successfully_false_names"])
    print("> Number of stocks in total:\t{total}".format(total=len(stocks_filtered)))
    print("> Number of stocks in queue:\t{queue}".format(queue=len(stocks_filtered)-(stocks_parsed["successfully"] + stocks_parsed["successfully_false"])))
    print("> Number of nicely parsed:\t{parsed}".format(parsed=stocks_parsed["successfully"]))
    print("> Number of poorly parsed:\t{parsed}".format(parsed=stocks_parsed["successfully_false"]))
    print("> Crawling Progression:\t\t{progress:.2%}".format(progress=(stocks_parsed["successfully"] + stocks_parsed["successfully_false"])/len(stocks_filtered)))
    print("> Time to go (ETA):\t\t~{eta:.0f} minutes\n".format(eta=((len(stocks_filtered)-(stocks_parsed["successfully"] + stocks_parsed["successfully_false"]))*average_crawling_delay*7)/60)) # guessing

def filter_output(stocks_filtered, average_crawling_delay):
    print("\n  Welcome to StockPyrate and here we go...\n")
    print("> Time to go (ETA): {eta:.0f} minutes".format(eta=(len(stocks_filtered)*average_crawling_delay*7)/60)) # guessing
    print("> Number of stocks:", len(stocks_filtered))
    [print("- {name}\t({sector})\t| {index}".format(name=name.upper(), sector=sector.split("> ")[1], index=index.upper()).expandtabs(43)) for name, symbol, sector, index in stocks_filtered]

def sneak_preview(stock_objects, override_analysis_only_df_crawling):
    if not override_analysis_only_df_crawling:
        print("\n> Sneak Preview:")
        [print(key[1].tail(), "\n") for key in stock_objects[-1].dataframes_for_xlsx_export.items() if "row_count" not in str(key[0]) and ("overview" in str(key[0]) or "daily" in str(key[0]))]

def show_time_series_dataframes(time_series_dataframes_for_all_stocks, override_analysis_only_df_crawling):
    if override_analysis_only_df_crawling:
        [print("Stock: "+str(stock_key).upper()+"\n",dataframe.tail(),"\n") for stock_key, dataframe in time_series_dataframes_for_all_stocks.items()]

def concatenation(code, argument=""):
    code_args_one = {}
    code_args_one[1] = "\n>>> Starting concatenation of xlsx files in subfolder ", argument.upper(), "\n\n"
    code_args_one[2] = "- Reading: ", argument[int(str(argument).rfind("\\"))+1:], "\n"
    code_args_one[3] = "- Writing: ", argument[int(str(argument).rfind("\\"))+1:].replace("..", ""), "\n- HAPPY END\n\n"
    code_args_one[4] = "- Ups, nothing here! Please provide XLSX files to be concatenated.\n\n"
    [print(i, end = "") for i in code_args_one[code]]

def xlsx(xlsx_filename):
    print("> Writing XLSX file (check subfolder 'xlsx'):\n-", xlsx_filename)