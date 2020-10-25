## StockPyrate
A Yahoo Finance stock crawler for financial data analysis and visualization with Excel/XSLX file export.

![StockPyrate.py](https://github.com/MarcelFrank/StockPyrate/blob/main/demo/screenshot-from-example-xlsx-02.png)

## About
StockPyrate is a python script to gather stock information about quotes, dividends and corporate statistics on Yahoo Finance. As a user you are allowed to enter a list of stocks or indices to be crawled, parsed, analyzed and exported. The script returns xls files for each stock and/or index component with data metrics and visualization e. g. current dividend yield or delta percentage for highs and lows of preset time periods. It further provides a function to concatenate exported files into just a single one to get an overview of all stocks at one place.

## Important (cookie required)
- Methodically the script relies on a slow, old-fashioned approach of web scraping instead of rapid API calls. The current implementation sends requests to the german subdomain of Yahoo Finance which requires your consent to its data policy, technically done by a cookie. It thus forces you to visit Yahoo Finance on your own with a common browser beforehand to initially set consent values that you easily need to enter and save before starting the script ([cf. setup.md](setup/setup.md)).
- XLS content e. g. sheet/column captions (currently) 100% german.

## Requirements
Python 3.7.6 (maybe Python 3.5+ does the job). To run StockPyrate you need:

- **Requests** (for crawling)
- **BeautifulSoup** (for parsing)
- **Pandas** (for exporting)

Other modules come with the standard Python package such as datetime, random or os ([cf. requirements.txt](/requirements.txt)).

## How to run
1. Set up your cookie in crawler.py (/functions)
2. Define stock names to parse in stockpyrate.py (root).
3. Hit play.

**crawler.py:**
```
# Define your cookie values by replacing the empty strings. Done!

def create_cookie():
    cookie = {
        'EuConsent': '',                       
        'UIDR': '', [...]
```

**stockpyrate.py:**
```
# Define your stock names to parse as list of strings. Done!

custom_filter["stocks_whitelist"] = ["intel"]  
```

## Demo and Setup
Take a look into the /demo folder to watch StockPyrate.py crawling and parsing "Intel" (or start animated GIF [here](demo/demo-run-just-executing-from-commandline.gif)) and the corresponding exported XLSX file. Apart from module requirements you initially need to set up your individual cookie - and you are ready to go ([cf. setup.md](setup/setup.md)).

## Feature list

**Crawling and Parsing**
- Whitelist filter for stock symbols
- Blacklist filter for stock symbols
- Whitelist filter for stock indices
- Blacklist filter for stock indices
- Timer in seconds for average crawling delay
- Status messages steadily commenting on what is going on
- Error handling primarily to avoid stalling ("in case of misunderstanding, read on!")
- Automated user-friendly file naming convention for xls export
- Custom filename and folder for xlsx concatenation procedure
- Predefined list of stocks
- Once started, crawl, parse, analyze and export in one shot
- Nice loops in range of your decent purposes

**Financial Data Analysis and Visualization**
- Current stock quote
- Current dividend
- Current dividend yield
- Ex date
- Daily stock quotes with line chart
- Avg. weekly stock quotes with line chart
- Avg. quarterly stock quotes with line chart
- Dividend history with column chart
- Transaction volumes in number of trades shares
- Transaction amounts, cf. above multiplied with closing prices
- Free float market capitalization history
- Percentage of delta of daily/weekly/quarterly changes
- Visualization of Ups and Downs with arrow symbols
- High, mean, low stock quote, date and percent delta for 1 week
- High, mean, low stock quote, date and percent delta for 2 weeks
- High, mean, low stock quote, date and percent delta for 1 month...
- ... up to 15 years
- Number of days a stock needs to recover its before-ex-date-price after dividend payment.
- Key facts based on statistics section at Yahoo Finance

**Excel/XSLX file export**
- Includes all financial data cf. above
- One XLSX file for each stock
- Exported sheets contain:
<br>&nbsp;1. Key data
<br>&nbsp;2. Daily Stock Prices
<br>&nbsp;3. Weekly Stock Prices
<br>&nbsp;4. Quarterly Stock Prices
<br>&nbsp;5. Dividends History
<br>&nbsp;6. Transaction Volume 12 Months
<br>&nbsp;7. Transaction Volume History
<br>&nbsp;8. Market Capitalization
- Optional output of one single xlsx file containing key facts of all stocks.

## Tasks
- Refactoring.
- Translation.
- Write documentation.
- Change from german subsite to US site.
- More stocks/indices.
- Integrate financial data such as income statements (SEC fillings).
- Make it more versatile (untie the Yahoo-biased parsing, other sources).
- Rebuild or additional feature: API calls.
- Build web frontend.

## Contribution
- Find and report bugs.
- Give ideas on data analysis.

## License

This project is licensed under the terms of the [GPL-3.0](https://github.com/MarcelFrank/StockPyrate/blob/main/LICENSE).
