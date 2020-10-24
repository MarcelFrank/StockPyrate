from functions import stocks_db, runtimer, status_messages

def start_workflow(stock_current, stock_objects):
    stopwatch = runtimer.TimeKeeper()
    stopwatch.start()
    stock_objects = add_stock_object(stock_current["name"], stock_objects)
    import_parsed_data(stock_current, stock_objects[-1])
    render_financial_data(stock_objects[-1])
    export_to_xls(stock_objects[-1])
    status_messages.code_args_none(2)
    stopwatch.show()

def add_stock_object(share_name, stock_objects):
    status_messages.status(201)    
    stock_objects += [stocks_db.StockObject(share_name)]
    #stock_objects_dictionary[share_name] = stock_objects[-1]
    return stock_objects

def import_parsed_data(share, stock_object_current):
    stock_object_current.write_raw_dictionary_data_to_stock_object(share)
    
def render_financial_data(stock_object_current):
    stock_object_current.compute_dividend_rate()
    stock_object_current.compute_volume_transaction_daily()
    stock_object_current.assign_overview_shares_total()
    stock_object_current.assign_overview_shares_freefloat()
    stock_object_current.assign_overview_ex_date()
    stock_object_current.compute_market_capitalization_daily()
    stock_object_current.compute_market_capitalization_quarterly()
    stock_object_current.compute_volume_transaction_one_year()
    stock_object_current.compute_volume_transaction_quarterly()
    stock_object_current.compute_prices_with_delta_by_timestamp()
    stock_object_current.compute_prices_with_delta_by_row()
    stock_object_current.compute_race_to_recuperate_dividend()
    stock_object_current.assign_overview_key_facts()

def export_to_xls(stock_object_current):
    stock_object_current.create_pandas_dataframes()
    stock_object_current.create_xlsx()