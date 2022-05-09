import json
import urllib.request
import os
import time
import datetime

import pandas as pd

api_key = os.getenv('FMP_KEY')

class Stock:
        def __init__(self,inpt):
                self.inp = inpt



def ticker_list(ak):
        """ return list of all ticker usable in the tool"""
        URL = "https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey="+str(ak)
        data = urllib.request.urlopen(URL)
        data = data.read().decode("utf-8")
        data = data.replace('"', '')
        tick = data.strip('][').split(', ')
        return tick

def incomeStatement(ak,tick):
        """ return list of dict containing icnome statement data"""
        URL =" https://financialmodelingprep.com/api/v3/income-statement/"+str(tick)+"?apikey="+str(ak)
        data = urllib.request.urlopen(URL)
        data  = data.read().decode("utf-8")
        data = eval(data)
        return data

def balanceSheet(ak,tick):
        """ return list of dict containing balance sheet statement data"""
        URL =" https://financialmodelingprep.com/api/v3/balance-sheet-statement/"+str(tick)+"?apikey="+str(ak)
        data = urllib.request.urlopen(URL)
        data  = data.read().decode("utf-8")
        data = eval(data)
        return data

def cashFlow(ak,tick):
        """ return list of dict containing cash flow statement data"""
        URL =" https://financialmodelingprep.com/api/v3/cash-flow-statement/"+str(tick)+"?apikey="+str(ak)
        data = urllib.request.urlopen(URL)
        data  = data.read().decode("utf-8")
        data = eval(data)
        return data

def ratio(ak,tick):
        """ return list of dict containing financial ratio data in trailing 12 month"""
        URL =" https://financialmodelingprep.com/api/v3/ratios-ttm/"+str(tick)+"?apikey="+str(ak)
        data = urllib.request.urlopen(URL)
        data  = data.read().decode("utf-8")
        data = eval(data)
        return data

def dividend(ak,tick):
        """ return list of dict containing financial ratio data in trailing 12 month"""
        URL =" https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/"+str(tick)+"?apikey="+str(ak)
        data = urllib.request.urlopen(URL)
        data  = data.read().decode("utf-8")
        data = eval(data)
        return data


def profile(ak,tick):
        """ return list of dict containing profile data of the company"""
        URL =" https://financialmodelingprep.com/api/v3/profile/"+str(tick)+"?apikey="+str(ak)
        data = urllib.request.urlopen(URL)
        data  = data.read().decode("utf-8")
        data = data.replace('false','False')
        data = data.replace('true','True')
        data = eval(data)
        return data[0]

'''def news(ak,tick):
        """ return list of dict containing news about the stock"""
        articles =[]
        for i in range(50):
                page = str(i)
                URL =" https://financialmodelingprep.com/api/v3/fmp/articles?page="+page+"&size=5/&apikey="+str(ak)
                data = urllib.request.urlopen(URL)
                data  = data.read().decode("utf-8")
                data = data.replace('false', 'False')
                data = data.replace('true', 'True')
                data = eval(data)['content']
                article = [i if tick in i['tickers'] else '' for i in data]
                for j in article:
                        if j =='':
                                pass
                        else:
                                articles.append(j)
                time.sleep(.5)
        return articles'''

def price(ak,tick,freq):
        """ return historical price of the stock at given time frequency"""
        URL = " https://financialmodelingprep.com/api/v3/historical-chart/"+freq+"/" + str(tick) + "?apikey=" + str(ak)
        data = urllib.request.urlopen(URL)
        data = data.read().decode("utf-8")
        data = eval(data)
        return data

def price_vol(ak,tick):
        """ return historical price of the stock with differential data"""
        URL = " https://financialmodelingprep.com/api/v3/historical-price-full/" +str(tick) + "?apikey=" + str(ak)
        data = urllib.request.urlopen(URL)
        data = data.read().decode("utf-8")
        data = eval(data)
        return data['historical']

def news_(nk,tick):
        """return news about the specified ticker"""
        dt =datetime.datetime.today()-datetime.timedelta(days=7)
        dt = dt.strftime("%Y-%m-%d")
        URL = "https://newsapi.org/v2/everything?q="+str(tick)+"&from="+str(dt)+"&sortBy=publishedAt&language=en&it&apiKey="+str(nk)
        data = urllib.request.urlopen(URL)
        data = data.read().decode("utf-8")
        data = data.replace('false', 'False')
        data = data.replace('true', 'True')
        data = data.replace('null', 'None')
        data = eval(data)
        return data['articles']

def Option(key,tick):
        """return a list of dict containing data of ticker's vanilla options"""
        td = datetime.datetime.today().strftime("%Y-%m-%d")
        om = (datetime.datetime.today()+datetime.timedelta(days=90)).strftime("%Y-%m-%d")
        URL = "https://eodhistoricaldata.com/api/options/"+str(tick)+"?api_token="+str(key)+"&from="+td+"&to="+om
        data = urllib.request.urlopen(URL)
        data = data.read().decode("utf-8")
        data = data.replace('FALSE', 'False')
        data = data.replace('TRUE', 'True')
        data = data.replace('null', 'None')
        data = eval(data)
        opt = data['data']
        df = pd.DataFrame()
        for t in range(len(opt)):
                for i in opt[t]['options']:
                        for j in (opt[0]['options'][i]):
                                j['date'] = opt[t]['expirationDate']
                                df = pd.concat([df,pd.DataFrame(j,index=[0])],ignore_index=True)
        df = df.drop(['contractName','updatedAt','contractSize','contractPeriod','currency','lastTradeDateTime'],axis=1)
        for i in opt:
                print(i['expirationDate'])
        return df