import pandas as pd
import numpy as np


pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)


def backtest(df_original: pd.DataFrame, tenkan_period: int, kijun_period: int):
    """
    long signal:
    >tenkan_senkou_a cross kijun_senkou_a upwards
    >the close price is above the ichimoku cloud
    >chikou span is trending upwards

    short signal:
    <tenkan_senkou_a cross kijun_senkou_a downwards
    <the close price is below the ichimoku cloud
    <chikou span is trending downwards
     
    tijd om te gaan slapen

    """
    df = df_original.copy()
    # Tenkan Sen : Short-term signal line

    df["rolling_min_tenkan"] = df["low"].rolling(window=tenkan_period).min()
    df["rolling_max_tenkan"] = df["high"].rolling(window=tenkan_period).max()

    df["tenkan_sen"] = (df["rolling_max_tenkan"] + df["rolling_min_tenkan"]) / 2

    df.drop(["rolling_min_tenkan", "rolling_max_tenkan"], axis=1, inplace=True)

    # Kijun Sen : Long-term signal line

    df["rolling_min_kijun"] = df["low"].rolling(window=kijun_period).min()
    df["rolling_max_kijun"] = df["high"].rolling(window=kijun_period).max()

    df["kijun_sen"] = (df["rolling_max_kijun"] + df["rolling_min_kijun"]) / 2

    df.drop(["rolling_min_kijun", "rolling_max_kijun"], axis=1, inplace=True)

    # Senkou Span A

    df["senkou_span_a"] = ((df["tenkan_sen"] + df["kijun_sen"]) / 2).shift(kijun_period)

    # Senkou Span B

    df["rolling_min_senkou"] = df["low"].rolling(window=kijun_period * 2).min()
    df["rolling_max_senkou"] = df["high"].rolling(window=kijun_period * 2).max()

    df["senkou_span_b"] = ((df["rolling_max_senkou"] + df["rolling_min_senkou"]) / 2).shift(kijun_period)

    df.drop(["rolling_min_senkou", "rolling_max_senkou"], axis=1, inplace=True)

    # Chikou Span : Confirmation line

    df["chikou_span"] = df["close"].shift(kijun_period)

    df.dropna(inplace=True)

    # Signal
    """
     Tenkan Sen - Kijun Sen = positive if bullish trend is present and negative if bearish trend is present
     ( if this column is positive it means the tenkan is above the kijun if negative it means the tenkan is below the kijun)
    """

    df["tenkan_minus_kijun"] = df["tenkan_sen"] - df["kijun_sen"]  
    df["prev_tenkan_minus_kijun"] = df["tenkan_minus_kijun"].shift(1)

    df["signal"] = np.where((df["tenkan_minus_kijun"] > 0) &
                            (df["prev_tenkan_minus_kijun"] < 0) &
                            (df["close"] > df["senkou_span_a"]) &
                            (df["close"] > df["senkou_span_b"]) &
                            (df["close"] > df["chikou_span"]), 1,

                            np.where((df["tenkan_minus_kijun"] < 0) &
                            (df["prev_tenkan_minus_kijun"] > 0) &
                            (df["close"] < df["senkou_span_a"]) &
                            (df["close"] < df["senkou_span_b"]) &
                            (df["close"] < df["chikou_span"]), -1, np.NaN))  # -1 = sell, 1 = buy, 0 = not satisfied do nothing
    df = df[df["signal"] != 0].copy()                                 

    df["pnl"] = df["close"].pct_change() * df["signal"].shift(1)

    df["cum_pnl"] = df["pnl"].cumsum()
    df["max_cum_pnl"] = df["cum_pnl"].cummax()
    df["drawdown"] = df["max_cum_pnl"] - df["cum_pnl"]

    return df["pnl"].sum(), df["drawdown"].max()