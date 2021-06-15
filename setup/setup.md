## Step 1 of 3 - edit crawler.py (for enabling)

To get StockPyrate running on the german subdomain of Yahoo Finance it is necessary to edit the content of the function "create_cookie()" located in file "crawler.py" (cf. folder "functions"). The empty string values you find in the "cookie = {}" dictionary need to be replaced. One method: Initialize the values beforehand by visiting Yahoo Finance with a common browser, e. g. Chrome, on your own hand. Cf. screenshots give-consent*.jpg in folder "/setup" to see where to find these values. Then copy and paste your client-specific values into the dictionary in "create_cookie()". Sorry for this inconvinience. All necessary keys are listed here:

``` 
def create_cookie():
    cookie = {
        'EuConsent': '',
        'UIDR': '',
        'UID': '',
        'ucs': '',
        'GUCS': '',
        'APIDTS': '',
        'CP3': '',
        'APID': '',
        'A1': '',
        'A1S': '',
        'A3': '',
        'B': ''
    }
    return cookie
```

## Step 2 of 3 - edit stockpyrate.py (for crawling and parsing)

To define the stocks to be parsed please enter a list of stock names (as list of strings) in the first line of the user's control panel. That's it. Since it does not ask for stock symbols, rather stock names, just have a look into the alphabetically sorted stock list in functions/stock_userlist.py. Alternatively you may enter e. g. "semiconductors" or "gaming" into the third row (whitelist_sectors) and let StockPyrate pick all related stocks for you automatically.

Before starting to crawl it is useful to set override_crawling_print_stocklist to "True" to just print out the selected stocks. Crawled stocks will be exported to XLSX files automatically into folder /XLSX. You can merge these files afterwards by setting override_crawling_merge_xlsx_files to "True" and running the script again, building one xlsx file out of all xlsx files currently located in folder /XLSX.

```
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

```

## Step 3 of 3 - run stockpyrate.py

Run stockparser.py e. g. directly from prompt/cmd or hitting the play button in e. g. Visual Studio Code. XLS folder and file names will be generated automatically. Status messages will keep you updated on what the script is doing.
