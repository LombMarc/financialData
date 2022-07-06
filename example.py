import os
from Stock import Stock
import numpy as np
from reader import *


ak = os.getenv('FMP_KEY')  #https://financialmodelingprep.com free api key
nk = os.getenv('NEWS_KEY') #https://newsapi.org free api key plan
opKey = os.getenv('EODKEY') #https://eodhistoricaldata.com premium api key plan (20$ for option data)

# The api key can be saved as environmental variable or stored as a string variable in the script itself

if __name__=='__main__':
    apl = Stock('AAPL')
    print(apl)
    apl = Options('AAPL')
    print(apl.iloc[0])
    
# This example will retrive the overall summary for the Apple stocks and then will show information for the option with smaller time to maturity.
