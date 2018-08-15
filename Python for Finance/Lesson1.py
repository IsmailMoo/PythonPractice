# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 10:49:20 2018

@author: Home-PC
"""

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.finance import candlestick_ohlc 
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web
import os
import bs4 as bs
import pickle
import requests

style.use('ggplot')

##############################P1  reading stock data from api
def get_data_from_api(file,):
    start = dt.datetime(2000,1,1)
    end = dt.datetime(2018,7,19)
    
    df = web.DataReader('CTSH', 'morningstar', start, end)
    #df.head(5)

    df.to_csv(file)


data_path = 'C:\\Users\\Home-PC\\Python for Finance\\Data\\'
file = os.path.join(data_path, 'CTSH.csv')

#get_data_from_api(file)

##############################P2 reading data from csv & pandas ploting
#read data from CSV
csv_df = pd.read_csv(file,index_col='Date',parse_dates=True)

csv_df.head(5)
csv_df.tail(5)
#csv_df.plot()
plt.show()

csv_df.iloc[range(len(csv_df)-100,len(csv_df),1) ,:]

#csv_df.iloc[range(len(csv_df)-100,len(csv_df),1) ,1].plot()
#csv_df.iloc[range(len(csv_df)-100,len(csv_df),1) ,2].plot()
#csv_df.iloc[range(len(csv_df)-100,len(csv_df),1) ,3].plot()
#csv_df.iloc[range(len(csv_df)-100,len(csv_df),1) ,4].plot()
#csv_df.iloc[range(len(csv_df)-100,len(csv_df),1) ,5].plot()
#plt.show()


##############################P3  ploting & sub ploting, moving avg using matplotlib
csv_df['100ma'] = csv_df['Close'].rolling(window=100, min_periods=0).mean()
# rolling() will moving avg 
csv_df['100mm'] = csv_df['Close'].rolling(window=100, min_periods=0).median()
#csv_df.dropna(inplace=True)

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1,sharex=ax1)

ax1.plot(csv_df.index, csv_df['Close'])
ax1.plot(csv_df.index, csv_df['100ma'])
ax1.plot(csv_df.index, csv_df['100mm'])
ax2.plot(csv_df.index, csv_df['Volume'])
#plt.show()
file = os.path.join(data_path, 'moving_avg.svg')
plt.savefig(file,format='svg')

##############################P4  resample 
df_ohlc = csv_df['Close'].resample('10D').ohlc()
#resample give sample of given window
#ohlc avg open-high-low-close values, 
df_volume = csv_df['Volume'].resample('10D').sum()
df_ohlc.reset_index(inplace=True)

df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1,sharex=ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
plt.show()

df_ohlf.head(5)
df_volume.head(5)
csv_df['Close'].head(10)


##############################P5   
def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
        
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
        
    print(tickers)
    
    return tickers













