from datetime import datetime

def get_urls(symbol):
    current_unix_time = str(int(datetime.timestamp(datetime.now())))
    base_url = "https://de.finance.yahoo.com/quote/"
    urls = {}
    urls["url_weeks"] = base_url+symbol+"/history?p="+symbol
    urls["url_months"] = base_url+symbol+"/history?period1=1561939200&period2="+current_unix_time+"&interval=1wk&filter=history&frequency=1wk"
    urls["url_years"] = base_url+symbol+"/history?period1=1104537600&period2="+current_unix_time+"&interval=3mo&filter=history&frequency=1mo"
    urls["url_dividends"] = base_url+symbol+"/history?period1=946684800&period2="+current_unix_time+"&interval=div%7Csplit&filter=div&frequency=1mo"
    urls["url_statistics"] = base_url+symbol+"/key-statistics?p="+symbol
    urls["url_unixtime"] = current_unix_time
    return urls

def update_unixtime(share):
    current_unix_time = str(int(datetime.timestamp(datetime.now())))
    share["url_months"] = share["url_months"].replace(share["url_unixtime"], current_unix_time)
    share["url_years"] = share["url_years"].replace(share["url_unixtime"], current_unix_time)
    share["url_dividends"] = share["url_dividends"].replace(share["url_unixtime"], current_unix_time)
    share["url_unixtime"] = current_unix_time
    return share