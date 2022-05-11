from reader import *
from os import getenv
import pandas as pd

ak = getenv('FMP_KEY')

class Stock:

    def __init__(self,ticker):   #1 request
        """
        :param kwargs: 'ticker'; from this everything is drawn
        the whole class make a total of 9 requests, is possible to end up with more request using the HistPriceFreq, on which we can freely selct the desired time frequency.
        """
        self.ticker = ticker
        Profile = profile(ak, self.ticker)
        self.name = Profile['companyName']
        self.price = Profile['price']
        self.currency = Profile['currency']
        self.dscrpt = Profile['description']
        self.industry = Profile['industry']
        self.sector = Profile['sector']
        self.sesReturn = Profile['changes']
        self.ipo = Profile['ipoDate']

        self.range = Profile['range']  #52 week high-low
        self.beta = Profile['beta']
        self.cap = Profile['mktCap']
        self.volu = Profile['volAvg']
        self.div  = Profile['lastDiv']
        self.exchg = Profile['exchangeShortName']
        self.DCF = Profile['dcf']
        self.diffDCF = Profile['dcfDiff']

    def Ratio(self):                #1 request
        ratios = ratio(ak,self.ticker)
        self.ratio = pd.DataFrame(ratios)

    def finStat(self):  #3 request
        IncomeStatement = pd.DataFrame(incomeStatement(ak,self.ticker))
        IncomeStatement = IncomeStatement.drop(columns=['symbol','cik','fillingDate','acceptedDate','calendarYear','period','link','finalLink'])
        self.IncomeStatement = IncomeStatement

        BalanceSheet = pd.DataFrame(balanceSheet(ak,self.ticker))
        BalanceSheet = BalanceSheet.drop(columns=['symbol','cik','fillingDate','acceptedDate','calendarYear','period','link','finalLink'])
        self.BalanceSheet =BalanceSheet

        CashFlow = pd.DataFrame(cashFlow(ak,self.ticker))
        CashFlow = CashFlow.drop(columns=['symbol','cik','fillingDate','acceptedDate','calendarYear','period','link','finalLink'])
        self.CashFlow = CashFlow

    def News(self): #1 request on news
        LastNews = pd.DataFrame(news_(nk,self.ticker))
        LastNews= LastNews.drop(columns=['source','urlToImage','content'])
        self.lsNews = LastNews

    def HistPriceFreq(self,freq):    #1 request
        Price = pd.DataFrame(price(ak,self.ticker,freq))
        Price = Price.set_index('date')
        self.histPrice = Price

    def HistPrice(self):  #4 request
        Price = pd.DataFrame(price(ak,self.ticker,'1min'))
        Price = Price.set_index('date')
        self.Price1min = Price

        Price = pd.DataFrame(price(ak, self.ticker, '1hour'))
        Price = Price.set_index('date')
        self.Price1hour = Price

        Price = pd.DataFrame(price(ak, self.ticker, '4hour'))
        Price = Price.set_index('date')
        self.Price4hour = Price

        Price = pd.DataFrame(price_vol(ak, self.ticker))
        Price = Price.set_index('date')
        Price = Price.drop('label')
        self.Price1day = Price

    def HistDividen(self): # 1 request
        histDivd = pd.DataFrame(dividend(ak,self.ticker)['historical'],columns=['date','adjDividend','dividend'])
        histDivd = histDivd.set_index('date')
        self.historicalDividend = histDivd

    def __str__(self):
        self.Ratio()
        self.finStat()
        self.News()
        to_ret =" name: %s | ticker: %s \n description: %s \n industry: %s | sector: %s | currency: %s | exchange: %s\n 52 week range: %s | last price: %f | last return: %f | last dividend: %f \n beta: %f | volume: %f | MktCap: %f \n " \
                " -----------------------------------------------------------------------------------\n" \
                " Balance Sheet:\n" \
                "%s \n" \
                "-----------------------------------------------------------------------------------\n"\
                "Income statement:\n" \
                "%s \n" \
                "-----------------------------------------------------------------------------------\n" \
                "Cashflow statement:\n" \
                "%s" \
                " -----------------------------------------------------------------------------------\n" \
                "main ratio: \n" \
                "%s \n " \
                "-----------------------------------------------------------------------------------\n" \
                "Latest news:\n" \
                "%s" %(self.name,self.ticker,self.dscrpt,self.industry,self.sector,self.currency,self.exchg,self.range,self.price,self.sesReturn,self.div,self.beta,self.volu,self.cap,self.BalanceSheet.to_string(),self.IncomeStatement.to_string(),self.CashFlow.to_string(),self.ratio.to_string(),self.lsNews.to_string())

        return to_ret






            
            

