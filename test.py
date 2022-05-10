import time
import numpy as np

from database import Hdf5Client
from utils import *

pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)


# import and format the data
h5_db = Hdf5Client("binance")
data = h5_db.get_data("BTCUSDT",from_time=0, to_time=int(time.time() * 1000))
data = resample_timeframe(data,"1h")


"""
Backtest a simple strategy 
Will go long when the close price of the candle is above the average of the high and low of this candle.
and the revers situatio, when the close price is below the average of the high and low  of this candle we will go short.
"""
# perform operations on the DataFrame
data["high_low_avg"] = (data["high"] + data["low"]) / 2
data['signal'] = np.where(data['close'] > data['high_low_avg'], 1, 0)
print(data)
