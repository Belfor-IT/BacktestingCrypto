import datetime
import time
import requests
import pandas as pd
import numpy as np
from math import floor
from termcolor import colored as cl
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethirtyeight')
plt.figure(figsize=(12,10))
pd.set_option("display.max_rows", None, "display.max_columns", None)



def get_market_data(market, granularity):
    resp = requests.get('https://api.pro.coinbase.com/products/' + market + '/candles?granularity=' + str(granularity))
    if resp.status_code != 200:
        raise Exception(format(resp.json()['message']))
    else:
        df = pd.DataFrame(resp.json(), columns=[ 'epoch', 'low', 'high', 'open', 'close', 'volume' ])
        df = df.iloc[::-1].reset_index()
        df.to_csv('BTC-EUR.csv')
        return df

def write_to_csv(df):
    df.to_csv('BTC-EUR.csv')
    return df

def get_local_data(Data_csv):
    df = pd.read_csv(Data_csv)
    return df


def get_macd(price, slow, fast, smooth):
    exp1 = price.ewm(span = fast, adjust = False).mean()
    exp2 = price.ewm(span = slow, adjust = False).mean()
    macd = pd.DataFrame(exp1 - exp2).rename(columns = {'close':'macd'})
    signal = pd.DataFrame(macd.ewm(span = smooth, adjust = False).mean()).rename(columns = {'macd':'signal'})
    hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns = {0:'hist'})
    frames =  [macd, signal, hist]
    df = pd.concat(frames, join = 'inner', axis = 1)
    return df



def plot_macd(prices, macd, signal, hist):
    ax2 = plt.subplot2grid((8,1), (5,0), rowspan = 3, colspan = 1)
    ax2.plot(macd, color = 'grey', linewidth = 1.5, label = 'MACD')
    ax2.plot(signal, color = 'skyblue', linewidth = 1.5, label = 'SIGNAL')

    for i in range(len(prices)):
        if str(hist[i])[0] == '-':
            ax2.bar(prices.index[i], hist[i], color = '#ef5350')
        else:
            ax2.bar(prices.index[i], hist[i], color = '#26a69a')

    plt.legend(loc = 'lower right')

def plot_linear_channels(df, macd):
    ax1 = plt.subplot2grid((8,1), (0,0), rowspan = 5, colspan = 1)
    x = df.index
    y = df['close']
    (m, b) = np.polyfit(x, y, 1)
    yp = np.polyval([m, b], x)
    highchannel = yp + np.std(yp)
    lowchannel = yp - np.std(yp)
    ax1.plot(yp, color = 'blue')
    ax1.plot(highchannel, color = 'red')
    ax1.plot(lowchannel, color = 'green')
    ax1.grid(True)
    #ax1.scatter(x,y, color = 'black')
    ax1.set_title('Linear Channels')
    ax1.set_ylabel('Price')
    xl = df.index


    #if df['close'] > highchannel:
    for i in range(len(df)):
        if df['close'][i] > highchannel[i]:
            ax1.scatter(xl[i], df['close'][i], color = 'red')
        elif df['close'][i] < lowchannel[i] and macd[i] < 0.0:
            ax1.scatter(xl[i], df['close'][i], color = 'green')
        else:
            ax1.scatter(xl[i], df['close'][i], color = 'black')

    # for i in range(len(df)):
    #     if df['close'][i] < lowchannel[i] and macd[i] < 0.0:
    #         ax1.scatter(xl[i], df['close'][i], color = 'green')

        # elif df['close'][i] < lowchannel[i]:
        #     ax1.scatter(xl[i], lowchannel[i], color = 'green')
            # if df['close'][i] > highchannel[i]:
            #     ax1.scatter(xl[i], df['close'][i], color = 'red')
            # else:
            #     ax1.scatter(xl[i], df['close'][i], color = 'red')
    
    # for p in df['close']:
    #     for lowC in lowchannely
    #         if p > lowC:
    #             print('lowC', lowC)
    #             print('p', p)
    #             # print('buy')
            # elif p < lowC and p > highchannel:
            #     print('lowC', lowC)
            #     print('p', p)
            #     print('sell')


#df = get_market_data('BTC-EUR', 900)
df = get_local_data('BTC-EUR.csv')
df.head()
Test_macd = get_macd(df['close'], 26, 12, 9)
print('Hier printen we de MACD', Test_macd['macd'])
Test_macd.tail()
plot_macd(df['close'], Test_macd['macd'], Test_macd['signal'], Test_macd['hist'])
plot_linear_channels(df,Test_macd['macd'])
plt.show()