from functions import execute, parser, runtimer, status_messages, stocks_testdata, yahoo_ini
from bs4 import BeautifulSoup
import random, requests, time

stock_current = {}
stock_objects = []
stocks_parsed = {}
stocks_parsed["successfully"] = 0
stocks_parsed["successfully_names"] = []
stocks_parsed["successfully_false"] = 0
stocks_parsed["successfully_false_names"] = []
stocks_parsed["time_series_dataframes_for_all_stocks_access_by_stock_name_as_key"] = {}

def get_html(url, header, cookie, average_crawling_delay):
    seconds = random.randint(1, (average_crawling_delay*2)-1)
    status_messages.crawler_get(seconds, url)
    time.sleep(float(seconds))
    r = requests.Session()
    response = r.get(url, headers=header, cookies=cookie, timeout=60.0)
    html = BeautifulSoup(response.text, "html.parser")
    return html

def initiate_loop_for_crawling_analysis_and_export(stocks_filtered, average_crawling_delay, override_crawling_use_testdata, override_analysis_only_df_crawling):
    for stock in stocks_filtered:
        stock_current["name"]   = stock[0]
        stock_current["id"]     = stock[1].split(".")[0] # set to stock symbol w/o exchange location
        stock_current["symbol"] = stock[1]
        stock_current["sector"] = stock[2]
        stock_current["index"]  = stock[3]   
        args = (
            stock_current,
            stocks_parsed,
            stock_objects,
            average_crawling_delay,
            stocks_filtered,
            override_crawling_use_testdata,
            override_analysis_only_df_crawling
            )

        try_to_get_stock(*args) # runs the entire procedure of crawling, analysis and xlsx export if not overriden

    return stocks_parsed["time_series_dataframes_for_all_stocks_access_by_stock_name_as_key"]

def try_to_get_stock(
        stock_current,
        stocks_parsed,
        stock_objects,
        average_crawling_delay,
        stocks_filtered,
        override_crawling_use_testdata,
        override_analysis_only_df_crawling
        ):
    try:
        # Crawling       
        stock_current = initiate_crawling(stock_current, average_crawling_delay, override_crawling_use_testdata)
        # Financial Analysis and XLSX Export
        execute.intitiate_analysis_and_export(stock_current, stock_objects, override_analysis_only_df_crawling)
        # Save time series dataframe for current stock to dictionary if crawling has been successful (dict will be returned after full run of initiate_loop_for_crawling_analysis_and_export()).
        stocks_parsed["time_series_dataframes_for_all_stocks_access_by_stock_name_as_key"][stock_current["name"]] = stock_objects[-1].time_series_dataframe
        # Status Messaging
        stocks_parsed["successfully"] += 1
        stocks_parsed["successfully_names"].append(stock_current["name"])
        status_messages.sneak_preview(stock_objects, override_analysis_only_df_crawling)            
        status_messages.crawler_progression(stocks_filtered, stocks_parsed, average_crawling_delay)

    except IndexError:
        status_messages.crawler_error(410, stock_current, stocks_parsed)
    except ZeroDivisionError:
        status_messages.crawler_error(420, stock_current, stocks_parsed)
        stock_objects.pop(-1)
    except KeyError:
        status_messages.crawler_error(430, stock_current, stocks_parsed)
        stock_objects.pop(-1)
    except ValueError:
        status_messages.crawler_error(440, stock_current, stocks_parsed)
    except AttributeError:
        status_messages.crawler_error(450, stock_current, stocks_parsed)

def initiate_crawling(stock_current, average_crawling_delay, override_crawling_use_testdata):
    stopwatch = runtimer.TimeKeeper()
    stopwatch.start()
    
    status_messages.crawler_task(stock_current)
    header = create_header()
    cookie = create_cookie()
    urls = yahoo_ini.get_urls(stock_current["symbol"])
    stock_current.update(urls)
    
    if override_crawling_use_testdata != True:
        html = get_html(stock_current["url_statistics"], header, cookie, average_crawling_delay)
        stock_current["statistics"] = parser.stock_statistics(html)
        html = get_html(stock_current["url_weeks"], header, cookie, average_crawling_delay)
        stock_current["stock_price_weeks"], stock_current["stock_volume_weeks"] = parser.stock_history(html)
        stock_current = yahoo_ini.update_unixtime(stock_current)          
        html = get_html(stock_current["url_months"], header, cookie, average_crawling_delay) 
        stock_current["stock_price_months"], stock_current["stock_volume_months"] = parser.stock_history(html)
        stock_current = yahoo_ini.update_unixtime(stock_current)
        html = get_html(stock_current["url_years"], header, cookie, average_crawling_delay)
        stock_current["stock_price_years"], stock_current["stock_volume_years"] = parser.stock_history(html)
        stock_current = yahoo_ini.update_unixtime(stock_current)
        html = get_html(stock_current["url_dividends"], header, cookie, average_crawling_delay)
        stock_current["dividends"] = parser.stock_dividends(html)
    else:
        stock_current["statistics"] = stocks_testdata.get("statistics")
        stock_current["stock_price_weeks"], stock_current["stock_volume_weeks"] = stocks_testdata.get("weekly_prices"), stocks_testdata.get("weekly_volume")
        stock_current["stock_price_months"], stock_current["stock_volume_months"] = stocks_testdata.get("monthly_prices"), stocks_testdata.get("monthly_volume")
        stock_current["stock_price_years"], stock_current["stock_volume_years"] = stocks_testdata.get("yearly_prices"), stocks_testdata.get("yearly_volume")
        stock_current["dividends"] = stocks_testdata.get("dividends")

    status_messages.status(301)
    stopwatch.show()

    return stock_current

def create_header():
    headers = [
        {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://de.finance.yahoo.com',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        },
        {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://de.finance.yahoo.com',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.58'        
        }
    ]
    header = random.choice(headers)
    return header

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