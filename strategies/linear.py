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



def plot_macd(prices, macd, signal, hist, df):
    ax1 = plt.subplot2grid((8,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((8,1), (5,0), rowspan = 3, colspan = 1)
    ax1.plot(prices)
    # ax1.plot(prices + np.std(prices), color='red')
    # ax1.plot(prices - np.std(prices), color='red')
    #sns.lineplot(x=x_rp, y=y_rp + np.std(y_rp), color='b')
    #sns.lineplot(x=x_rp, y=y_rp + np.std(y_rp), color='b')

    ax2.plot(macd, color = 'grey', linewidth = 1.5, label = 'MACD')
    ax2.plot(signal, color = 'skyblue', linewidth = 1.5, label = 'SIGNAL')

    for i in range(len(prices)):
        if str(hist[i])[0] == '-':
            ax2.bar(prices.index[i], hist[i], color = '#ef5350')
        else:
            ax2.bar(prices.index[i], hist[i], color = '#26a69a')

    plt.legend(loc = 'lower right')


df = get_local_data('BTC-GBP.csv')
df.head()
x = df.index
y = df['close']
(m, b) = np.polyfit(x, y, 1)
#(m, b) = np.polyval(x, y, 1)
print(m, b)
yp = np.polyval([m, b], x)
plt.plot(x, yp)
plt.grid(True)
plt.scatter(x,y)
plt.show()




# Test_macd = get_macd(df['close'], 26, 12, 9)
# Test_macd.tail()
# plot_macd(df['close'], Test_macd['macd'], Test_macd['signal'], Test_macd['hist'], df)
# plt.show()