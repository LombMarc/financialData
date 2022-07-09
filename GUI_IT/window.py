from italian_reader import *
import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk


def Window():
    sym_list = pd.read_csv('/Users/marcolombardi/Desktop/QF_COPY/pythonFinancialModelling/scripts/database_holder/BI_symbol.csv')

    window = tk.Tk()
    window.title("Stock Summary")
    window.geometry("1080x720")
    window.minsize(1080, 720)
    window.maxsize(1080, 720)
    window.configure(background='#b6c8de')

    left_frame = tk.Frame(window,height=710,width=530,bg='#c0d3eb',bd=5)
    left_frame.place(x=5,y=5)
    right_frame = tk.Frame(window,height=710,width=535,bg='#c0d3eb',bd=5)
    right_frame.place(x=540,y=5)



    def get_data():
        clean_r = tk.Canvas(right_frame,height=720,width=520,bg='#b6c8de',bd=0)
        clean_r.place(x=0,y=30)
        clean_l = tk.Canvas(left_frame, height=420, width=520, bg='#b6c8de',bd=0)
        clean_l.place(x=0, y=280)
        symbol = str(sym_entry.get())
        tick = sym_list[sym_list['name'] == symbol]['symbol'].values[0]
        stk = Stock_yf(tick)
        name = tk.Label(left_frame, text=stk.name)
        name.place(x=10,y=40,width=270)
        sect = tk.Label(left_frame, text=("Sector: "+str(stk.sector)))
        sect.place(x=10,y=70)
        mkt_cap = tk.Label(left_frame, text=("Market Cap: "+str(stk.marketcap)))
        mkt_cap.place(x=140,y=70)
        beta = tk.Label(left_frame, text=("Beta= "+str(stk.beta)))
        beta.place(x=10,y=100)
        pe = tk.Label(left_frame, text=("PE= "+str(stk.ttm_eps)))
        pe.place(x=110,y=100)
        book_val = tk.Label(left_frame, text=("Book Value= "+str(stk.bookvalue)))
        book_val.place(x=160,y=100)
        out_share = tk.Label(left_frame, text=("Outstanding Shares= "+str(stk.out_share)))
        out_share.place(x=10,y=130)
        div = tk.Label(left_frame, text=("Dividend= "+str(stk.dividend)))
        div.place(x=10,y=160)
        range = tk.Label(left_frame, text=("52 Week Range= "+str(stk.range52)))
        range.place(x=110,y=160)

        def hist_bs():
            bs_fig = plt.Figure(figsize=(7.5,5),facecolor='#c0d3eb')
            bs_canva = FigureCanvasTkAgg(bs_fig, master=left_frame)

            ax = bs_fig.add_subplot()
            bs = stk.balance_sheet
            bs.plot(kind='bar', rot=15, grid=True, yticks=bs[bs.columns[0]], ax=ax,title='Balance Sheet')
            ax.get_yaxis().set_major_formatter(
                FuncFormatter(lambda x, p: format(int(x), ',')))

            ax.set_facecolor("#b6c8de")
            bs_canva.get_tk_widget().place(x=1, y=330)

        def hist_cf():
            bs_fig = plt.Figure(figsize=(7.5,5),facecolor='#c0d3eb')
            bs_canva = FigureCanvasTkAgg(bs_fig, master=left_frame)

            ax = bs_fig.add_subplot()
            ic = stk.cashflow
            ic['index'] = ['Operating Flows','Investing Flows','Financial Flows','Cash Flows']
            ic=ic.set_index('index')
            ic.plot(kind='bar', rot=15, grid=True, yticks=ic[ic.columns[0]], ax=ax,title="Cash Flow")
            ax.get_yaxis().set_major_formatter(
                FuncFormatter(lambda x, p: format(int(x), ',')))

            ax.set_facecolor("#b6c8de")
            bs_canva.get_tk_widget().place(x=1, y=330)

        def hist_ic():
            bs_fig = plt.Figure(figsize=(7.5,5),facecolor='#c0d3eb')
            bs_canva = FigureCanvasTkAgg(bs_fig, master=left_frame)

            ax = bs_fig.add_subplot()
            ic = stk.income_statement.loc[['Total Revenue', 'Cost Of Revenue', 'Gross Profit', 'Ebit', 'Net Income']]
            ic.plot(kind='bar', grid=True, rot=15, yticks=ic[ic.columns[0]], ax=ax,title="Income Statement")
            ax.get_yaxis().set_major_formatter(
                FuncFormatter(lambda x, p: format(int(x), ',')))
            ax.set_facecolor("#b6c8de")
            bs_canva.get_tk_widget().place(x=1, y=330)

        def y_price():

            bs_fig = plt.Figure(figsize=(6.5, 4), facecolor='#c0d3eb')
            bs_canva = FigureCanvasTkAgg(bs_fig, master=right_frame)

            ax = bs_fig.add_subplot()
            bs = stk.historical_price['Close'].iloc[-252:]
            bs.plot(rot=15, grid=True,  ax=ax, title='1 year Price')

            ax.set_facecolor("#b6c8de")
            bs_canva.get_tk_widget().place(x=5, y=35)

        def y3_price():

            bs_fig = plt.Figure(figsize=(6.5, 4), facecolor='#c0d3eb')
            bs_canva = FigureCanvasTkAgg(bs_fig, master=right_frame)

            ax = bs_fig.add_subplot()
            bs = stk.historical_price['Close'].iloc[-756:]
            bs.plot(rot=15, grid=True,  ax=ax, title='3 year Price')

            ax.set_facecolor("#b6c8de")
            bs_canva.get_tk_widget().place(x=5, y=35)

        def ratio_lab():
            rt = stk.ratio
            rt = rt.transpose()
            rt = rt.to_string(justify='center')
            rt_label = tk.Label(right_frame, text=rt,background="#b6c8de")
            rt_label.place(x=60, y=380)


        bs_button = tk.Button(left_frame, text="Balance Sheet", command=lambda: hist_bs())
        bs_button.place(x=10,y=280,width=100)
        cf_button = tk.Button(left_frame, text="Income Statement", command=lambda: hist_ic())
        cf_button.place(x=130,y=280,width=130)
        cf_button = tk.Button(left_frame, text="Cash Flows", command=lambda: hist_cf())
        cf_button.place(x=280, y=280,width=100)
        year_button = tk.Button(right_frame, text="Yearly Price", command=lambda: y_price())
        year_button.place(x=5,y=1)
        y3_button = tk.Button(right_frame, text="3 Year Price", command=lambda: y3_price())
        y3_button.place(x=130,y=1)
        rat_btn = tk.Button(left_frame, text="Ratios", command=lambda: ratio_lab())
        rat_btn.place(x=400,y=280)






    button = tk.Button(left_frame, text="enter", command=get_data)
    button.place(x=215, y=5,width=60,height=25)
    sym_entry = AutocompleteCombobox(left_frame, sym_list['name'].tolist())
    sym_entry.place(x=5, y=5)


    window.mainloop()

if __name__=='__main__':
    Window()