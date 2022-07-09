import bs4 as bs
import requests
import pandas as pd
import time
import tqdm
import pandas_datareader as pdr
from reader import *
import os

ak = os.getenv('FMP_KEY')
idx = ['A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
url = lambda a,num: "https://www.borsaitaliana.it/borsa/azioni/listino-a-z.html?initial="+str(a)+"&page="+str(num)

def name_frame():
    links = []
    names = []
    for a in ['A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
        for i in ['1','2','3','4','5','6','7','8','9']:
            df = pd.DataFrame()
            page = requests.get(url(a, i))
            soup = bs.BeautifulSoup(page.text,'lxml')
            table = soup.find('table')
            for tr in table.findAll("tr"):
                trs = tr.findAll("td")
                for each in trs:
                    try:
                        link = (each.find("a")['href'])
                        name = each.find("strong").text
                        names.append(name)
                        if "imposta-alert.html" in link:
                            pass
                        elif "borsa-virtuale" in link:
                            pass
                        else:
                            links.append(link)
                    except:
                        pass
    df['name'] = names
    df['link'] = links
    return df

def add_symbol():
    df = pd.read_csv('/Users/marcolombardi/Desktop/QF_COPY/pythonFinancialModelling/scripts/database_holder/BI_scraper.csv')
    df = df.drop_duplicates('name')
    print(df)
    symbol = []
    for i in tqdm.tqdm(range(len(df))):
        url = df['link'].iloc[i]
        try:
            ddf = pd.read_html(url)
            sym = ddf[1].iloc[4]
            #print(sym)
            symbol.append(sym[1])

        except:
            symbol.append(None)
        #time.sleep(.5)
    df['symbol'] = symbol
    print(df)
    return df

def fm_symb():
    tick_list = ticker_list(ak)
    mi_list = [i if str(i).endswith(".MI") else None for i in tick_list]
    mi_list = [i for i in mi_list if i is not None]
    df = pd.read_csv('/Users/marcolombardi/Desktop/QF_COPY/pythonFinancialModelling/scripts/database_holder/BI_symbol.csv')
    ak_lis = []
    for i in df['symbol'].tolist():
        if i in mi_list:
            ak_lis.append(i)
        else:
            ak_lis.append('0')
    df['AV_symbol'] = ak_lis
    return df

# only 85 symbol traded on euronext.MI are present in the financuial modelling api

