import pandas as pd
import yfinance as yf
import numpy as np

def symbol(path):
    """ return df of symbol and company name"""
    return pd.read_csv(path)

df = symbol('/Users/marcolombardi/Desktop/QF_COPY/pythonFinancialModelling/scripts/database_holder/BI_symbol.csv')
#print(df['symbol'])

def daily_price(symbol):
    """ return df of last price """
    return yf.download(symbol, period='1d')

def historical_price(symbol):
    """ return df of historical price """
    return yf.download(symbol, period='max')

def balance_sheet_extend(symbol):
    """ return df of balance sheet """
    l = ['Cash', 'Short Term Investments', 'Net Receivables', 'Inventory', 'Other Current Assets',
         'Total Current Assets', 'Long Term Investments', 'Property Plant Equipment', 'Good Will', 'Intangible Assets',
         'Other Assets', 'Total Assets', 'Short Long Term Debt', 'Accounts Payable', 'Other Current Liab',
         'Total Current Liabilities', 'Long Term Debt', 'Deferred Long Term Liab', 'Other Liab', 'Total Liab',
         'Common Stock', 'Treasury Stock', 'Other Stockholder Equity', 'Retained Earnings', 'Net Tangible Assets',
         'Capital Surplus', 'Total Stockholder Equity']

    df = yf.Ticker(symbol).get_balance_sheet().fillna(0)
    df= df.reindex(l)
    return df

def balance_sheet(symbol):
    """ return df of balance sheet with summary information"""
    l = ['Total Current Assets','Total Assets',
         'Total Current Liabilities', 'Total Liab', 'Total Stockholder Equity']
    df = yf.Ticker(symbol).balance_sheet.fillna(0).loc[l]
    m = ['Current Assets', 'Non Current Assets',
         'Current Liabilities', 'Non Current Liab', 'Stockholder Equity']
    df.loc['Total Assets'] = df.loc['Total Assets']-df.loc['Total Current Assets']
    df.loc['Total Liab'] = df.loc['Total Liab']-df.loc['Total Current Liabilities']
    df = df.set_index(pd.Series(m))
    return df

def income_statement(symbol):
    """ return df of income statement """
    l = ["Selling General Administrative", "Total Revenue", "Cost Of Revenue", "Gross Profit", "Research Development",
         "Selling General Administrative", "Non Recurring", "Other Operating Expenses", "Total Operating Expenses",
         "Operating Income", "Total Other Income Expense Net", "Ebit", "Interest Expense", "Income Before Tax",
         "Income Tax Expense", "Net Income From Continuing Ops", "Discontinued Operations", "Extraordinary Items",
         "Effect Of Accounting Charges", "Other Items", "Net Income", "Minority Interest",
         "Net Income Applicable To Common Shares"]
    df = yf.Ticker(symbol).get_financials().fillna(0)
    df = df.reindex(l)
    return df

def cashflow(symbol):
    """ return df of cashflow """
    l = ["Total Cash From Operating Activities", "Total Cashflows From Investing Activities","Total Cash From Financing Activities","Change In Cash"]
    df = yf.Ticker(symbol).get_cashflow().fillna(0).loc[l]
    return df

def Options(symbol):
    """Input a ticker to get a dataframe containing all the traded option data, the index is set to the expiration date,
     so to retrive a subset of the dataframe  use the df.loc['date in format yyyy-mm-dd'] method."""
    tik = yf.Ticker(symbol)
    expir = tik.options
    options = []
    for e in expir:
        opt = tik.option_chain(e)
        C = pd.DataFrame(opt.calls)
        P = pd.DataFrame(opt.puts)
        C['type'] = 'C'
        P['type'] = 'P'
        Opt = pd.concat([C, P])
        Opt['expiration'] = e
        Opt = Opt.set_index('expiration')
        options.append(Opt)
    try:
        option = pd.concat(options)
        print("Maturity: ", expir)
        return option
    except:
        print("No options found")
        return None

def news_link(symbol):
    pd.set_option('display.max_colwidth', None)
    df = yf.Ticker(symbol).news
    df = [(df[i]['title'],df[i]['link']) for i in range(len(df))]
    df = pd.DataFrame(df, columns=['title','link'])
    return df

def ratios(bs,ic,cf):
    '''bs = balance_sheet_extend(symbol)
    ic = income_statement(symbol)
    cf = cashflow(symbol)'''
    liquidity_rt = {
        'Liquidity Ratios':['-' for i in range(len(bs.columns))],
        'Current Ratio': round(bs.loc['Total Current Assets']/bs.loc['Total Current Liabilities'],2),
        'Acid-Test Ratio': round((bs.loc['Total Current Assets']-bs.loc['Inventory'])/bs.loc['Total Current Liabilities'],2),
        'Cash Ratio': round(bs.loc['Cash']/bs.loc['Total Current Liabilities'],2),
        'Operating Cash Flow Ratio': round(cf.loc['Total Cash From Operating Activities']/bs.loc['Total Current Liabilities'],2),
        'Leverage Ratios':['-' for i in range(len(bs.columns))],
        'Debt Ratio': round(bs.loc['Total Liab']/bs.loc['Total Assets'],2),
        'Debt to Equity Ratio': round(bs.loc['Total Liab']/bs.loc['Total Stockholder Equity'],2),
        'Interest Coverage Ratio': round(ic.loc['Ebit']/np.abs(ic.loc['Interest Expense']),2),
        'Debt Service Coverage Ratio': round(ic.loc['Operating Income']/(bs.loc['Short Long Term Debt']+bs.loc['Long Term Debt']),2),
        'Efficiency Ratios':['-' for i in range(len(bs.columns))],
        'Asset Turnover Ratio': round((ic.loc['Total Revenue'])/bs.loc['Total Assets'],2),
        'Inventory Turnover Ratio': round(ic.loc['Cost Of Revenue']/bs.loc['Inventory'],2),
        'days Sale in Inventory Ratio': round(365/(ic.loc['Cost Of Revenue']/bs.loc['Inventory']),2),
        'Profitability Ratios':['-' for i in range(len(bs.columns))],
        'Gross Margin Ratio': round(ic.loc['Gross Profit']/(ic.loc['Total Revenue']),2),
        'Operating Margin Ratio': round(ic.loc['Operating Income']/(ic.loc['Total Revenue']),2),
        'Return on Assets': round(ic.loc['Net Income']/bs.loc['Total Assets'],2),
        'Return on Equity': round(ic.loc['Net Income']/bs.loc['Total Stockholder Equity'],2)
    }
    year = [str(i)[:4] for i in bs.columns]

    Df = pd.DataFrame(liquidity_rt)
    Df.index = year

    return Df

class Stock_yf:
    def __init__(self, symbol):
        self.symbol = symbol
        info = yf.Ticker(symbol).info
        stat = yf.Ticker(symbol).stats()
        try:
            self.currency = stat['financialData']['financialCurrency']
        except:
            self.currency = 'USD'
        try:
            self.name = info['longName']
        except:
            self.name = info['shortName']
        try:
            self.sector = info['sector']
            self.industry = info['industry']
        except:
            self.sector = '-'
            self.industry = '-'
        self.marketcap = info['marketCap']
        try:
            self.description = info['longBusinessSummary']
        except:
            self.description = '-'
        self.range52 = (info['fiftyTwoWeekLow'], info['fiftyTwoWeekHigh'])
        try:
            self.dividend = stat['defaultKeyStatistics']['lastDividendValue']
        except:
            self.dividend = 0
        if self.dividend == None:
            self.dividend = 0

        try:
            self.out_share = stat['defaultKeyStatistics']['sharesOutstanding']
        except:
            self.out_share = 0
        try:
            self.bookvalue = stat['defaultKeyStatistics']['bookValue']
        except:
            self.bookvalue = 0
        try:
            self.price_book = stat['defaultKeyStatistics']['priceToBook']
        except:
            self.price_book = 0
        try:
            self.ttm_eps = stat['defaultKeyStatistics']['trailingEps']
        except:
            self.ttm_eps = 0
        try:
            self.beta = stat['defaultKeyStatistics']['beta']
            if self.beta == None:
                self.beta = 0
        except:
            self.beta = 0
        self.balance_sheet = balance_sheet(symbol)
        self.balance_sheet_extend = balance_sheet_extend(symbol)
        self.income_statement = income_statement(symbol)
        self.cashflow = cashflow(symbol)
        self.tax_rate = self.income_statement.loc['Income Tax Expense'] / self.income_statement.loc['Net Income']
        self.fcf = self.cashflow.loc["Total Cash From Operating Activities"] + self.income_statement.loc[
            'Interest Expense'] * (1 - self.tax_rate) - self.cashflow.loc['Total Cashflows From Investing Activities']
        self.ratio = ratios(self.balance_sheet_extend, self.income_statement, self.cashflow)

        #self.news = news_link(symbol)
        self.historical_price = historical_price(symbol)
        self.options = Options(symbol)


    def __str__(self):
        to_ret =" name: %s | symbol: %s \n description: %s \n industry: %s | sector: %s \n 52 week range: %f %f  | last dividend: %f | beta: %f | MktCap: %f \n " \
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
                "%s \n" \
                "-----------------------------------------------------------------------------------\n" \
                "Latest news:\n" \
                "" % (
                self.name,self.symbol,self.description,self.industry,self.sector,self.range52[0],self.range52[1],self.dividend,self.beta,self.marketcap,
                self.balance_sheet.to_string(),self.income_statement.to_string(),self.cashflow.to_string(),self.ratio.to_string()#,self.news.to_string()
        )
        return to_ret


