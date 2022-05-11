import pandas as pd
import numpy as np


pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)


def backtest(df: pd.DataFrame, ma_period: int):
    #On balance Volume strategy "obv"
    #obv_ma = moving average of the obv
    df["obv"] = (np.sign(df["close"].diff()) * df["volume"]).fillna(0).cumsum()
    df["obv_ma"] = round(df["obv"].rolling(window=ma_period).mean(), 2)
    
    #signal = obv_ma > obv buy = 1, else sell = -1
    #close_change = close price - close price of the next candle
    #pnl = close_change * signal_shift
    df["signal"] = np.where(df["obv"] > df["obv_ma"], 1, -1)
    df["close_change"] = df["close"].pct_change()
    df["signal_shift"] = df["signal"].shift(1)
    df["pnl"] = df["close"].pct_change() * df["signal"].shift(1)

    #Compare two pnl stragety A or B 
    #maximum cumulative pnl
    df["cum_pnl"] = df["pnl"].cumsum()
    df["max_cum_pnl"] = df["cum_pnl"].cummax()
    df["drawdown"] = df["max_cum_pnl"] - df["cum_pnl"]

    return df["pnl"].sum(), df["drawdown"].max()

    """
    maximum drawdown = (max_price - min_price) / max_price
    Stragety: as a performance indicor, the obv strategy is a moving average of the obv
    """