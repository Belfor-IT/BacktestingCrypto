import datetime
import requests
import time

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

%matplotlib inline


def get_market_data(market, granularity):
    resp = requests.get('https://api.pro.coinbase.com/products/' + market + '/candles?granularity=' + str(granularity))
    if resp.status_code != 200:
        raise Exception(format(resp.json()['message']))
    else:
        df = pd.DataFrame(resp.json(), columns=[ 'epoch', 'low', 'high', 'open', 'close', 'volume' ])
        df = df.iloc[::-1].reset_index()
        return df

        df = get_market_data('BTC-GBP', 86400)

        df.head()


sns.set(font_scale=1.5)
plt.figure(figsize=(12,10))
rp = sns.regplot(x=df.index, y='close', data=df, ci=None, color='r')

y_rp = rp.get_lines()[0].get_ydata()
x_rp = rp.get_lines()[0].get_xdata()
sns.lineplot(x=x_rp, y=y_rp + np.std(y_rp), color='b')
sns.lineplot(x=x_rp, y=y_rp - np.std(y_rp), color='b')

tsidx = pd.DatetimeIndex(pd.to_datetime(df['epoch'], unit='s'), 
dtype='datetime64[ns]', freq='D')
rp.set_xticklabels(tsidx, rotation=45)

plt.xlabel('')
plt.ylabel('Price')
plt.show()



