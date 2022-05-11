import os
from Stock import Stock
import numpy as np
from reader import *


ak = os.getenv('FMP_KEY')  #https://financialmodelingprep.com free api key
nk = os.getenv('NEWS_KEY') #https://newsapi.org free api key plan
opKey = os.getenv('EODKEY') #https://eodhistoricaldata.com premium api key plan (20$ for option data)

if __name__=='__main__':
    '''tick_list = ticker_list(ak)
    print(len(tick_list))'''
    #apl = Stock('AAPL')
    apl = Options('AAPL')
    print(apl.loc['2022-05-13'])