from functions import stocks_userlist, execute
custom_filter = {}

#________________________________________________________U S E R ' S - C O N T R O L - P A N E L___

custom_filter["stocks_whitelist"]  = ["intel"] # Enter stock name(s) to be parsed as a list of strings, e. g. ["gilead", "pfizer"] (cf. dict values in stocks_userlist.py for inspiration)
custom_filter["stocks_blacklist"]  = []        # Vice versa (NOT to be parsed).
custom_filter["indices_whitelist"] = []        # Enter index/indices to be parsed as a list of strings, e. g. ["dow", "dax"] (cf. dict keys in stocks_userlist.py for inspiration)
custom_filter["indices_blacklist"] = []        # Vice versa (NOT to be parsed).
average_crawling_delay             = 30        # Enter crawling delay in seconds as integer
concatenate_xlsx_after_parsing     = False     # Enter True to read the first sheet of all created xlsx files and compile one xlsx file as an overview data collection for all stocks. 
custom_filename                    = "birdseyeview.xlsx"
custom_folder                      = "xlsx_concatenated"

#________________________________________________________S T A R T - P R O G R A M_________________

stocks_userlist = stocks_userlist.get()
args = (
    custom_filter,
    average_crawling_delay,
    concatenate_xlsx_after_parsing,
    custom_filename,
    custom_folder,
    stocks_userlist
    )
execute.start_program(*args)