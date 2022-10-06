from datetime import date
import pandas as pd
from tkinter import *
from yahooquery import Ticker
import os


def save_to_csv(tickers_df):
    global file_name
    file_name = f'quotes_{date.today().strftime("%y%m%d")}.csv'
    tickers_df.to_csv(file_name,index=False)

def get_prices():
    global tickers_df
    tickers_df = pd.DataFrame(columns=['Ticker', 'Price', 'Date'])
    tickers_string = entry.get()
    tickers_string = tickers_string.replace(' ', '')
    tickers_list = tickers_string.split(',')
    tickers_list = [ticker.strip() for ticker in tickers_list]
    all_tickers = Ticker(tickers_list)
    prices = all_tickers.price
    for ticker in tickers_list:
        try: 
            price = prices[ticker]['regularMarketPrice']
            date = prices[ticker]['regularMarketTime']
        except:
            price = ''
            date = ''
        temp_df = pd.DataFrame({'Ticker':ticker,'Price':price,'Date':date}, index=[0])
        tickers_df = pd.concat([tickers_df,temp_df],ignore_index=True)
    save_to_csv(tickers_df)
    os.startfile(file_name)



if __name__ == "__main__":
# TODO: 1) Run by pressing enter    2) Load tickers from CSV    3) Choose saving location    4) Disable buttons before entry is filled
    master = Tk()
    stocks_list_box = StringVar()

    master.title('YF Quotes')
    master.resizable(width=False, height=False)

    Label(master, text="Tickers: ").grid(row=0, sticky=W)

    result2 = Label(master, text="", textvariable=stocks_list_box)

    entry = Entry(master)
    entry.grid(row=1, column=0, sticky='we')
    
    Label(master, text="").grid(row=2, sticky=W)
    
    Label(master, text="Guidelines:").grid(row=3, sticky=W)
    Label(master, text="1. Separate by commas").grid(row=4, sticky=W)
    Label(master, text="2. Tickers as represented in Yahoo Finance").grid(row=5, sticky=W)
    
    download = Button(master, text="Download Prices", command=get_prices)
    download.grid(row=10, column=0, columnspan=1, rowspan=1 ,sticky='we')

    open_file = Button(master, text="Open File", command=lambda: os.startfile(file_name))
    open_file.grid(row=12, column=0, columnspan=1, rowspan=1, sticky='we')

    open_folder = Button(master, text="Open Folder", command=lambda: os.startfile(os.getcwd()))
    open_folder.grid(row=14, column=0, columnspan=1, rowspan=1, sticky='we')

    copy_to_clipboard = Button(master, text="Copy to Clipboard", command=lambda: tickers_df.iloc[:,0:2].to_clipboard(index=False, header=False))
    copy_to_clipboard.grid(row=16, column=0, columnspan=1, rowspan=1, sticky='we')

    Label(master, text="v0.2", font=("Helvetica", 7)).grid(row=20, sticky= W)
    Label(master, text="2-Oct-22", font=("Helvetica", 7)).grid(row=20, sticky= E)


    mainloop()