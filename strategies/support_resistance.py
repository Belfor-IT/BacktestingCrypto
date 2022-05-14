import pandas as pd
import time
import numpy as np

import matplotlib.pyplot as plt
import mplfinance as mpf

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)


def backtest(df: pd.DataFrame, min_points: int, min_diff_points: int, rounding_nb: float, take_profit: float,
             stop_loss: float):

    candle_length = df.iloc[1].name - df.iloc[0].name

    pnl = 0
    max_pnl = 0
    trade_side = 0
    entry_price = None
    max_drawdown = 0

    df["rounded_high"] = round(df["high"] / rounding_nb) * rounding_nb
    df["rounded_low"] = round(df["low"] / rounding_nb) * rounding_nb

    price_groups = {"supports": dict(), "resistances": dict()}
    levels = {"supports": [], "resistances": []}
    last_high_low = {"supports": [], "resistances": []}
    resistances_supports = {"supports": [], "resistances": []}

    # Numpy Arrays

    highs = np.array(df["high"])
    lows = np.array(df["low"])
    rounded_highs = np.array(df["rounded_high"])
    rounded_lows = np.array(df["rounded_low"])
    closes = np.array(df["close"])
    times = np.array(df.index)

    row = {"high": highs, "low": lows, "rounded_high": rounded_highs, "rounded_low": rounded_lows, "close": closes}

    for i in range(len(highs)):

        index = times[i]

        for side in ["resistances", "supports"]:

            high_low = "high" if side == "resistances" else "low"

            if row["rounded_" + high_low][i] in price_groups[side]:

                grp = price_groups[side][row["rounded_" + high_low][i]]

                broken_in_last = 0

                if grp["start_time"] is None:

                    for c in last_high_low[side]:
                        if c > row[high_low][i] and side == "resistances":
                            broken_in_last += 1
                        elif c < row[high_low][i] and side == "supports":
                            broken_in_last += 1

                    if broken_in_last < 3:
                        grp["start_time"] = index

                if broken_in_last < 3 and (grp["last"] is None or index >= grp["last"] + min_diff_points * candle_length):
                    grp["prices"].append(row[high_low][i])

                    if len(grp["prices"]) >= min_points:
                        extreme_price = max(grp["prices"]) if side == "resistances" else min(grp["prices"])
                        levels[side].append([(grp["start_time"], extreme_price), (index, extreme_price)])
                        resistances_supports[side].append({"price": extreme_price, "broken": False})

                    grp["last"] = index

            else:
                broken_in_last = 0

                for c in last_high_low[side]:
                    if c > row[high_low][i] and side == "resistances":
                        broken_in_last += 1
                    elif c < row[high_low][i] and side == "supports":
                        broken_in_last += 1

                if broken_in_last < 3:
                    price_groups[side][row["rounded_" + high_low][i]] = {"prices": [row[high_low][i]], "start_time": index, "last": index}

            # Check whether price groups are still valid or not

            for key, value in price_groups[side].items():
                if len(value["prices"]) > 0:
                    if side == "resistances" and row[high_low][i] > max(value["prices"]):
                        value["prices"].clear()
                        value["start_time"] = None
                        value["last"] = None
                    elif side == "supports" and row[high_low][i] < min(value["prices"]):
                        value["prices"].clear()
                        value["start_time"] = None
                        value["last"] = None

            last_high_low[side].append(row[high_low][i])
            if len(last_high_low[side]) > 10:
                last_high_low[side].pop(0)

            # Check new trade

            for sup_res in resistances_supports[side]:
                entry_condition = row["close"][i] > sup_res["price"] if side == "resistances" else row["close"][i] < sup_res["price"]

                if entry_condition and not sup_res["broken"]:
                    sup_res["broken"] = True
                    if trade_side == 0:
                        entry_price = row["close"][i]
                        trade_side = 1 if side == "resistances" else -1

            # Check PNL

            if trade_side == 1:
                if row["close"][i] >= entry_price * (1 + take_profit / 100) or row["close"][i] <= entry_price * (1 - stop_loss / 100):
                    pnl += (row["close"][i] / entry_price - 1) * 100
                    trade_side = 0
                    entry_price = None
            elif trade_side == -1:
                if row["close"][i] <= entry_price * (1 - take_profit / 100) or row["close"][i] >= entry_price * (1 + stop_loss / 100):
                    pnl += (entry_price / row["close"][i] - 1) * 100
                    trade_side = 0
                    entry_price = None

            max_pnl = max(max_pnl, pnl)
            max_drawdown = max(max_drawdown, max_pnl - pnl)

    mpf.plot(df, type="candle", style="charles", alines=dict(alines=levels["resistances"] + levels["supports"]))
    plt.show()

    return pnl, max_drawdown





    """	Backtest strategy
    long signal: when the resistance is above the average of the high and low of this candle
    short signal: when the support is below the average of the high and low of this candle
    :param df: Dataframe with the following columns:
        - date: Date of the candle
        - open: Open price of the candle
        - high: High price of the candle
        - low: Low price of the candle
        - close: Close price of the candle
        - volume: Volume of the candle
    :param min_points: Minimum number of points to create a resistance or support example: 3 points is at least 3 candles to create a resistance or support 
    :param min_diff_points: Minimum difference between min_points and the number of points to create a resistance or support example: 7 points is at least 7 candles to create a resistance or support
    :param rounding_nb: round the price of the candle
    :param stop_loss: Stop loss percentage
    """



"""
Notes for myslef (not for others):
 iterrows: iterate over the rows of a DataFrame
    iteritems: iterate over the (index, value) pairs of a DataFrame
round(A/b)*b: round A to the nearest multiple of b
create variables to store information as you are in the for loop (e.g. grp, grp["prices"], grp["start_time"], grp["last"])
Python dictinary and list: can be combined to structure your data (https://docs.python.org/3/tutorial/datastructures.html)
"""	








