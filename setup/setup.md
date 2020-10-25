## Step 1 of 2

To get StockPyrate running on the german subdomain of Yahoo Finance it is necessary to edit the content of the function "create_cookie()" located in file "crawler.py" (cf. folder "functions"). Just fill the empty string values you find in the dictionary "cookie". Necessary keys are listed here:

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

The values must be set beforehand by visiting Yahoo Finance with a common browser, e. g. Chrome, on your own hand. Cf. both JPG files to see where the values will be located (and then to be copy&pasted into the function mentioned above) in the browser's console.

## Step 2 of 2

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
