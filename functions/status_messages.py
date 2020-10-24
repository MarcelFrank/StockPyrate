def status(key):
    code = {}
    code[111] = "- Parsing stock history..."
    code[112] = "- Parsing dividend history..."
    code[113] = "- Parsing statistics..."
    code[201] = "> Creating stock object:\n"
    code[211] = "- Writing ID...\n"
    code[212] = "- Writing stock symbol...\n"
    code[213] = "- Writing index information...\n"
    code[214] = "- Writing daily stock prices...\n"
    code[215] = "- Writing weekly stock prices...\n"
    code[216] = "- Writing quartery stock prices...\n"
    code[217] = "- Writing daily transaction volume...\n"
    code[218] = "- Writing dividend history...\n"
    code[219] = "- Writing statistics...\n"
    code[220] = "- Writing transaction volumeSchreibe Handelsvolumen auf Wochenbasis...\n"
    code[221] = "- Writing weekly transaction volume...\n"
    code[222] = "- Writing quarterly transaction volume...\n"
    code[231] = "- Extracting number of total shares (string conversion for value)...\n"
    code[232] = "! Number of total shares are unknown. Total shares are set to '1'...\n"
    code[233] = "- Extracting number of free float shares (string conversion for 'millions')...\n"
    code[234] = "- Extracting number of free float shares (string conversion for 'billions')...\n"
    code[235] = "- Number of free float share is set to same value as total shares...\n"
    code[236] = "! Number of total and free float shares are unknown. Free float shares are set to '1'...\n"
    code[241] = "- Extracting ex date (string conversion to datetime object)...\n"
    code[242] = "! Ex date is unknown. Ex date is set to January 01, 1980 (needs to be datetime object for XLS export)\n"
    code[243] = "- Computing current dividend yield...\n"
    code[244] = "! There is no dividend candy. Current dividend yield is set to '0.00%'.\n"
    code[245] = "! Last dividend was paid in last year or back in the past. Current dividend yield is set to '0.00%'.\n"
    code[251] = "- Computing daily transaction amount (shares * daily closing price)...\n"
    code[252] = "- Computing quarterly transaction amount (shares * average price)...\n"
    code[253] = "- Computing transaction amount for the last 12 months (shares * average price)...\n"
    code[258] = "! Number of shares is unknown and market cap is not given in statistics. Fubar. Market Cap is set to '1'.\n"
    code[259] = "! An error ocurred while trying to compute transaction (prices and dates are out of sync).\n"
    code[261] = "- Computing delta percentage compared to current price...\n"
    code[271] = "- Creating pandas dataframes...\n"
    code[281] = "- Inserting subfolder hereby hardcodedlynamed to 'xlsx'...\n"
    code[282] = "- Inserting custom folder as destination folder for concatenated xlsx files...\n"
    code[291] = "- Writing key facts to be inserted as first sheet in single xlsx files...\n"
    [print(i, end = "") for i in code[key]]

def xlsx(xlsx_filename):
    print("> Writing XLSX file (check subfolder 'xlsx'):\n-", xlsx_filename)

def report(stocks_parsed):
    print("\n________________________________________________________________________________")
    print("\n> Total number of successfully parsed stocks:", stocks_parsed["successfully"], "\n-", stocks_parsed["successfully_names"], "\n")
    print("> Total number of not so successfuly parsed stocks:", stocks_parsed["successfully_false"], "\n-", stocks_parsed["successfully_false_names"], "\n")

def success(stocks_parsed):
    print("> Successfully parsed stocks up to now:\n-", stocks_parsed["successfully_names"], end = "")

def skip(index):
    print("\n________________________________________________________________________________\n\n>>> Index", index.upper(), "is blacklisted and will be skipped...")

def code_args_none(code):
    code_args_none = {}
    code_args_none[1] = "\n> Crawling and parsing of html content of all urls above took (in seconds):\n- "
    code_args_none[2] = "> Writing stock object, computing financial data and writing xlsx file took (in seconds):\n- "
    [print(i, end = "") for i in code_args_none[code]]

def code_args_one(code, argument):
    code_args_one = {}
    code_args_one[1] = ""
    code_args_one[2] = "\n________________________________________________________________________________\n\n>>> ", str(argument["name"]).upper(), " is about to be analyzed...\n"
    code_args_one[3] = "\n________________________________________________________________________________\n\n>>> ", str(argument["name"]).upper(), " is blacklisted and will be skipped..."
    [print(i, end = "") for i in code_args_one[code]]

def concatenation(code, argument=""):
    code_args_one = {}
    code_args_one[1] = "________________________________________________________________________________\n\n>>> Starting concatenation of xlsx files in subfolder ", argument.upper(), "\n\n"
    code_args_one[2] = "- Reading: ", argument[int(str(argument).rfind("\\"))+1:], "\n"
    code_args_one[3] = "- Writing: ", argument[int(str(argument).rfind("\\"))+1:].replace("..", ""), "\n- HAPPY END\n\n"
    [print(i, end = "") for i in code_args_one[code]]

def crawler_get(argument_one, argument_two):
    return print("\n> Crawling starts in", argument_one, "seconds:\n- URL:", argument_two)

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

def sneak_preview(df):
    print("\nSneak Preview:")
    [print(key[1].head(), "\n") for key in df.items() if "row_count" not in str(key[0]) and ("overview" in str(key[0]) or "daily" in str(key[0]))]