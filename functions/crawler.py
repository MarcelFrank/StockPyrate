from functions import parser, yahoo_ini, stocks_db_actions, status_messages, runtimer
from bs4 import BeautifulSoup
import random, requests, time

def get_html(url, header, cookie, average_crawling_delay):
    seconds = random.randint(1, (average_crawling_delay*2)-1)
    status_messages.crawler_get(seconds, url)
    time.sleep(float(seconds))
    r = requests.Session()
    response = r.get(url, headers=header, cookies=cookie, timeout=60.0)
    html = BeautifulSoup(response.text, "html.parser")
    return html

def create_header():
    headers = [
        {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Referer': '',
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
            'Referer': '',
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

def try_to_get_stock(
        stock_current,
        stocks_parsed,
        stock_objects,
        average_crawling_delay
        ):
    try:       
        stock_current = start_crawler(stock_current, average_crawling_delay)
        stocks_db_actions.start_workflow(stock_current, stock_objects)  
        stocks_parsed["successfully"] += 1
        stocks_parsed["successfully_names"].append(stock_current["name"])
        status_messages.success(stocks_parsed)
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

def start_crawler(stock_current, average_crawling_delay):
    stopwatch = runtimer.TimeKeeper()
    stopwatch.start()
    
    status_messages.code_args_one(2, stock_current)    
    header = create_header()
    cookie = create_cookie()
    urls = yahoo_ini.get_urls(stock_current["symbol"])
    stock_current.update(urls)
    
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

    status_messages.code_args_none(1)
    stopwatch.show()
    return stock_current