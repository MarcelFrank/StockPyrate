from functions import execute

custom_filter = {}

#________________________________________________________U S E R ' S - C O N T R O L - P A N E L___

custom_filter["whitelist_stocks"]  = ["intel"]
custom_filter["whitelist_indices"] = []
custom_filter["whitelist_sectors"] = []
custom_filter["blacklist_stocks"]  = []
custom_filter["blacklist_indices"] = []
average_crawling_delay             = 20

#________________________________________________________S P E C I A L - C O M M A N D S___________

override_filter_crawl_portfolio    = False # edit portfolio in stocks_userlist.py by insert lines from get_all_stocks() via copy&paste
override_analysis_only_df_crawling = False # crawling just returns a dataframe with prices for each stock skipping analysis and xlsx generation
override_crawling_print_stocklist  = False # display selected stocks and ETA according to custom filter settings and skip crawling
override_crawling_use_testdata     = False # pass stock_testdata.py to crawler for instant testing without internet connection
override_crawling_merge_xlsx_files = False # insert xlsx files of parsed stocks into default xlsx folder before setting to true
custom_filename                    = "merged.xlsx"
custom_folder                      = "xlsx_merged"

#________________________________________________________I N I T I A T E - P R O G R A M___________

args = (
    custom_filter,
    average_crawling_delay,
    custom_filename,
    custom_folder,
    override_filter_crawl_portfolio,
    override_crawling_print_stocklist,
    override_crawling_use_testdata,
    override_crawling_merge_xlsx_files,
    override_analysis_only_df_crawling
    )

execute.start(*args)