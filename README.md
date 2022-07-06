# Retriving financial data using api

The project use three free api to gather all sort of financia data, you can request the api key at
- https://financialmodelingprep.com for financial statements and historical data
- https://newsapi.org for news about the stock
- https://eodhistoricaldata.com (premium) for more option information

For the free user, the option data are retrived through the yahoo financa library.
Note that using the free api pricing there are limited number of request per day and the stock symbol acutally available are limited to the US stock market.

## How to use
Plug your api key in the variable present in the main.py script or save them as environment variable. Now choose the stock and the data you want, go on the reader.py to verify the name of the function you want to use.

- ticker_list: return list of all ticker usable
- incomeStatement: return list of dict containing income statement data,
- balanceSheet: return list of dict containing balace sheet data,
- cashFlow: return list of dict containing cash flow statement,
- ratio: return list of dict with main financial ratio,
- dividend: return list of dict for dividend data in trailing 12 month,
- profile: return general information about the company,
- price: return historical price at the given frequency,
- news_: return list of dict containing recent news including the ticker,
- Option_EOD (premium feature): return list of dict containing data for option whose underlying is the stock,
- Options: return a dataframe with all the option currently trading.

The Stock.py contain a class that include all relevant information for a given ticker, returning a proper summary of the company in term of financial statements, news and historical price.
