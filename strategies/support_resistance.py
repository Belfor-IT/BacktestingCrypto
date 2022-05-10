import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)


def backtest(df: pd.DataFrame, min_points: int, min_diff_points: int, rounding_nb: float, take_profit: float,
             stop_loss: float):
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

    candle_length = df.iloc[1].name - df.iloc[0].name

    df["rounded_high"] = round(df["high"] / rounding_nb) * rounding_nb
    df["rounded_low"] = round(df["low"] / rounding_nb) * rounding_nb

    price_groups = {"supports": dict(), "resistances": dict()}
    resistances_supports = {"supports": [], "resistances": []}

    for index, row in df.iterrows():

        for side in ["resistances", "supports"]:

            high_low = "high" if side == "resistances" else "low"

            if row["rounded_" + high_low] in price_groups[side]:

                grp = price_groups[side][row["rounded_" + high_low]]

                if index >= grp["last"] + min_diff_points * candle_length:
                    grp["prices"].append(row[high_low])

                    if len(grp["prices"]) >= min_points:
                        extreme_price = max(grp["prices"]) if side == "resistances" else min(grp["prices"])
                        resistances_supports[side].append({"price": extreme_price, "broken": False})

                    grp["last"] = index

            else:
                price_groups[side][row["rounded_" + high_low]] = {"prices": [row[high_low]], "start_time": index, "last": index}










