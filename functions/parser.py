from functions import converter, status_messages
from bs4 import BeautifulSoup
from datetime import datetime
import re

regex_dividend = re.compile("^Ta\\(c\\) Py\\(10px\\) Pstart\\(10px\\)$")
regex_dividend_date = re.compile("^Py\\(10px\\) Ta\\(start\\) Pend\\(10px\\)$")

def stock_history(corpus):
    status_messages.status(111)
    dates = []
    prices = []
    volumes = []
    stock_date_and_price = []
    stock_date_and_volume = []

    for row in corpus.select("tr"):            
        if len(row.contents) == 7 and row.contents[4].text != "-":
            dates.append(row.contents[0].text)
            prices.append(row.contents[4].text)
            volumes.append(row.contents[6].text)
    
    dates = dates[1:]
    prices = prices[1:]
    volumes = volumes[1:]
   
    dates = converter.to_date_object(dates)
    prices = [converter.to_float(price) for price in prices]
    volumes = [int((volume).replace("-", "1").replace(".", "")) for volume in volumes]

    for i in range(0, len(dates)):
        stock_date_and_price += [[dates[i], prices[i]]]
        stock_date_and_volume += [[dates[i], volumes[i]]]

    return stock_date_and_price, stock_date_and_volume

def stock_dividends(corpus):
    status_messages.status(112)
    dates = []
    dividends = []
    stock_date_and_dividends = []
  
    cells = corpus.find_all("td", class_=regex_dividend)
    for content in cells:
        dividend = content.text.replace("Dividende", "").replace(" ", "")    
        if dividend == "":     
            dividend = "0.0001"
        dividend = converter.to_float(dividend)
        dividends.append(dividend)
    
    cells = corpus.find_all("td", class_=regex_dividend_date)
    for content in cells:
        dates.append(content.text)
    dates = converter.to_date_object(dates)
    
    if dividends != []:
        for i in range(0,len(dates)):
            stock_date_and_dividends += [[dates[i], dividends[i]]] 
    else:
        string = "01.01.1980"
        dividend = "0.00"
        dividend = converter.to_float(dividend)
        stock_date_and_dividends = [[datetime.strptime(string, "%d.%m.%Y").date(), dividend]]

    return stock_date_and_dividends

def stock_statistics(corpus):
    status_messages.status(113)
    statistics = {}

    for content in corpus.select("tr"):
        key = content.find_next("span").text
        value = content.find_next("span").find_next("td").text
        statistics[key] = value
        
    return statistics