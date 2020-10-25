## Step 1 of 2 - edit crawler.py for enabling

To get StockPyrate running on the german subdomain of Yahoo Finance it is necessary to edit the content of the function "create_cookie()" located in file "crawler.py" (cf. folder "functions"). The empty string values you find in the "cookie = {}" dictionary need to be replaced. One method: Initialize the values beforehand by visiting Yahoo Finance with a common browser, e. g. Chrome, on your own hand. Cf. the both JPG give-consent*.jpg (cf. folder /setup) to give an idea where to find these values. Then copy and paste the it into "create_cookie()". All necessary keys are yet listed:

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

Sorry for this inconvinience.

## Step 2 of 2 - edit stockpyrate.py for parsing your desired stocks

To define the stocks to be parsed please enter a list of stock names (as strings) in the first dictionary key of the user's control panel. That's it. Since it does not ask for stock symbols, rather stock names, just have a look into the dictionaries in functions/stock_userlist.py where all accessible stock names are prefilled. Of course, you may enhance the stock_userlist.py by more stocks and give it a try.

```
#________________________________________________________U S E R ' S - C O N T R O L - P A N E L___

custom_filter["stocks_whitelist"]  = ["intel"]
custom_filter["stocks_blacklist"]  = []
custom_filter["indices_whitelist"] = []
custom_filter["indices_blacklist"] = []
average_crawling_delay             = 30
concatenate_xlsx_after_parsing     = False
custom_filename                    = "birdseyeview.xlsx"
custom_folder                      = "xlsx_concatenated"

```
