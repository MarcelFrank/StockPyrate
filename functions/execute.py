from functions import converter, crawler, financial_analysis, runtimer, status_messages, stocks_filter, stocks_userlist, xlsx_concatenation

def start(
    custom_filter,
    average_crawling_delay,
    custom_filename,
    custom_folder,
    override_filter_crawl_portfolio,
    override_crawling_print_stocklist,
    override_crawling_use_testdata,
    override_crawling_merge_xlsx_files,
    override_analysis_only_df_crawling
    ):
    if override_crawling_merge_xlsx_files:
        concatenate_xlsx(custom_filename, custom_folder)
    else:
        if override_crawling_use_testdata:
            custom_filter["whitelist_stocks"] = []
            stocks = stocks_userlist.get_testdata()
        elif override_filter_crawl_portfolio:
            stocks = stocks_userlist.get_portfolio()
        else:
            stocks = stocks_userlist.get_all_stocks()

        stocks_filtered = stocks_filter.apply(stocks, custom_filter)
        status_messages.filter_output(stocks_filtered, average_crawling_delay)
        
        if not override_crawling_print_stocklist:
            time_series_dataframes_for_all_stocks = crawler.initiate_loop_for_crawling_analysis_and_export(stocks_filtered, average_crawling_delay, override_crawling_use_testdata, override_analysis_only_df_crawling)
            status_messages.show_time_series_dataframes(time_series_dataframes_for_all_stocks, override_analysis_only_df_crawling)
                
def concatenate_xlsx(*args):
    try:
        xlsx_concatenation.shortcut(*args)
    except ValueError:
        status_messages.concatenation(4)

def intitiate_analysis_and_export(stock_current, stock_objects, override_analysis_only_df_crawling):
    stock_objects = add_stock_object(stock_current["name"], stock_objects)
    import_parsed_data(stock_current, stock_objects[-1])
    stock_objects[-1].time_series_dataframe = converter.create_time_series_dataframe_based_on_parsed_stock_data(stock_objects[-1])
    
    if not override_analysis_only_df_crawling:
        stopwatch = runtimer.TimeKeeper()
        stopwatch.start()
        render_financial_data(stock_objects[-1])
        export_to_xls(stock_objects[-1])
        status_messages.status(302)
        stopwatch.show()

def add_stock_object(stock_name, stock_objects):
    status_messages.status(201)
    stock_objects += [financial_analysis.StockObject(stock_name)]
    #stock_objects_dictionary[stock_name] = stock_objects[-1]
    return stock_objects

def import_parsed_data(stock, stock_object_current):
    stock_object_current.write_raw_dictionary_data_to_stock_object(stock)
   
def render_financial_data(stock_object_current):
    stock_object_current.compute_dividend_rate()
    stock_object_current.compute_volume_transaction_daily()
    stock_object_current.assign_overview_shares_total()
    stock_object_current.assign_overview_shares_freefloat()
    stock_object_current.assign_overview_ex_date()
    stock_object_current.compute_market_capitalization_daily()
    stock_object_current.compute_market_capitalization_all_shares_daily()
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