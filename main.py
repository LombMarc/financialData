import os
from Stock import Stock
import pandas as pd

from reader import ticker_list,incomeStatement,balanceSheet,cashFlow,ratio,dividend,profile,price,news_,price_vol

ak = os.getenv('FMP_KEY')
nk = os.getenv('NEWS_KEY')
if __name__=='__main__':
    #tick_list = ticker_list(ak)
    apl = Stock('AAPL')
    #apl = profile(ak,'aapl')
    print(apl)