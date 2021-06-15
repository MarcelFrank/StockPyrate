## Changelog

This is a version history with comments on recent updates. I am looking forward to rather build a new branch with a lot of changes at once than committing tiny tweaks.

## JUNE 15TH, 2021 - New branch called "update-2021-sectors-and-fixes" covering all changes in the last months

**New features:**
- SECTORS:<br />Sector of stock is written into xlsx output to add more information and better sorting.
- SECTOR FILTER:<br />Stock list to be passed to crawler can be chosen by sector using Yahoo terminology and assignments, e. g. all "semiconductors" stocks.
- PORTFOLIO FILTER:<br />Stock list to be passed to crawler can be chosen by predefined custom portfolio to quickly start crawling owned stocks without changing the more generic filter settings (just requires editing portfolio list beforehand).
- ESTIMATED TIME FOR CRAWLING:<br />Before crawling starts a list of stocks is displayed according to filter settings plus estimated crawling time updated after each crawled stock.
- STATUS MESSAGING:<br />Reworked the status messages with more insights on what the script is currently doing or why it could not export xlsx.
- TEST DATA:<br />More or less for debugging or mere demo the test data can be used for analyis and export without crawling - thus no internet connection required.

**Refactored:**
- List of stock to be crawled is now generated before crawling start instead of filtering while crawling loop is yet in progress.
- Restructured stock list by changing it from various dictionaries to one list, stock name and stock symbol position has been switched for better readablity.
- Loop for crawling way more simplified, not deeply nested as before.
- Functions reorganized and renamed putting code together by topics.
- Minor amendments in status messages.

**Corrections:**
- Update of stock symbols in stock list and added sectors, list contains over 600 stocks as of June 2021.
- Number of days to recover from "ex-date quote" to "last quote before ex-date" calculation in function compute_race_to_recuperate_dividend slightly improved.
- Added 30 columns of statistics into merged XLSX file missing up to now due to merge issue.
- Fixed the X-Axis in charts in single xlsx files for each stock now displaying readable dates instead of timestamps.

**Outlook:**
- Short term: Add Bollinger Bands (distance of quote-to-bands indicator) and Sharpe Ratio for several time spans. 
- Long term: Time series analysis with dataframes and API access - Currently StockPyrate uses beautifulsoup crawling and parsing capabilities generating somewhat ugly "lists" of stock data ([[Datetime1, Close1], [Datetime2, Close2], ...]) that are further analyzed with Python built-in functions. What a single Pandas function such as .pct_change() can do I coded out with bare hands - well, this happens to a beginner. In the current branch I refactored a lot of stuff yet to prepare the shift to a better approach: 1. Dataframes. 2. Time series analyis. 3. APIs. But this is a night owl project of a non-professional, so, it will take some time. To offer something yet the current model "stock data as python lists" is converted to a pandas dataframe with DateTimeIndex and Close Price as column (just in case you do not want to use an API, but crawling instead: look out for returned variable "time_series_dataframes_for_all_stocks" in execute.py which will allow further times series analysis). Then again, be aware of the restrictions in accuracy due to crawling: Only up to ~90 lines of quotes and volumes data is retrievable with one html request (cf. historical data section at Yahoo Finance, more data is loaded afterwards only when scrolling manually, "no can do"). Hence, the limited daily data is, once having passed 90 trading days, blended together with the average weekly and quarterly data points (yes, again only up to ~90, but ~90 quarters are 20+ years). Outcome: Accuracy for the last ~3-4 months will be daily, then frequency changes to weekly for around two years, then to quarterly for the last years. Of course, changing to dataframes and to APIs (AlphaVantage and IEXCloud to name it) will be the future of StockPyrate. Any comment highly appreciated, feel free to share your thoughts or projects.
