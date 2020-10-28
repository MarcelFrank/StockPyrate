from functions import crawler, status_messages, xlsx_concatenation

stock_current = {}
stock_objects = []
stocks_parsed = {}
stocks_parsed["successfully"] = 0
stocks_parsed["successfully_names"] = []
stocks_parsed["successfully_false"] = 0
stocks_parsed["successfully_false_names"] = []

#________________________________________________________M A I N - P R O G R A M___________________

def start_program(
    custom_filter,
    average_crawling_delay,
    concatenate_xlsx_after_parsing,
    custom_filename,
    custom_folder,
    stocks_userlist):

    if custom_filter["indices_whitelist"] == []:
        for key in stocks_userlist:
            custom_filter["indices_whitelist"].append(key)

    for index in custom_filter["indices_whitelist"]:
        if index not in custom_filter["indices_blacklist"]:
            stocks_of_selected_index = stocks_userlist[index]
            for i in list(range(0, len(stocks_of_selected_index))):
                stock_current["name"] = stocks_of_selected_index[i][1]
                if stock_current["name"] not in custom_filter["stocks_blacklist"] and (
                stock_current["name"] in custom_filter["stocks_whitelist"] or
                custom_filter["stocks_whitelist"] == []):
                    stock_current["id"] = i
                    stock_current["index"] = index
                    stock_current["symbol"] = stocks_of_selected_index[i][0]
                    args = (
                        stock_current,
                        stocks_parsed,
                        stock_objects,
                        average_crawling_delay
                        )
                    crawler.try_to_get_stock(*args)
                elif stock_current["name"] in custom_filter["stocks_blacklist"] + custom_filter["stocks_whitelist"] and (
                    custom_filter["stocks_blacklist"] != custom_filter["stocks_whitelist"]):
                    status_messages.code_args_one(3, stock_current)
        elif index in custom_filter["indices_blacklist"] + custom_filter["indices_whitelist"]:
            status_messages.skip(index)

    #________________________________________________________R E P O R T I N G_____________________

    if stocks_parsed["successfully"] + stocks_parsed["successfully_false"] != 0:
        status_messages.report(stocks_parsed)

    #________________________________________________________C O N C A T E N A T E - X L S X_______

    if concatenate_xlsx_after_parsing:
        xlsx_concatenation.shortcut(custom_filename, custom_folder)
