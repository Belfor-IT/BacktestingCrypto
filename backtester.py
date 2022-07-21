from database import Hdf5Client

from utils import resample_timeframe, STRAT_PARAMS
import strategies.obv
import strategies.ichimoku
import strategies.support_resistance


def run(exchange: str, symbol: str, strategy: str, tf: str, from_time: int, to_time: int):
    
    params_des = STRAT_PARAMS[strategy]

    params = dict()
    """
    p_name is short for parameter name example: "MA Period"
    p is short for parameter example:{"name": "MA Period", "type": int}
    """
    for p_code, p in params_des.items():
        while True:
            try:
                params[p_code] = p["type"](input(p["name"] + ": "))
                break
            except ValueError:
                continue

    if strategy == "obv":
        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = resample_timeframe(data, tf)

        pnl = strategies.obv.backtest(data, ma_period=params["ma_period"])
    # default 9 as moving average period
        #print(strategies.obv.backtest(data, 9))

        return pnl
    
    elif strategy == "ichimoku":
        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = resample_timeframe(data, tf)

        pnl = strategies.ichimoku.backtest(data, tenkan_period=params["tenkan"], kijun_period=params["kijun"])

        #print(strategies.ichimoku.backtest(data, tenkan_period=9, kijun_period=26))
        return pnl

    elif strategy == "sup_res":
        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = resample_timeframe(data, tf)

        pnl = strategies.support_resistance.backtest(data, min_points=params["min_points"],
                                                     min_diff_points=params["min_diff_points"],
                                                     rounding_nb=params["rounding_nb"],
                                                     take_profit=params["take_profit"], stop_loss=params["stop_loss"])
        
        #print(strategies.support_resistance.backtest(data, min_points=3, min_diff_points=7, rounding_nb=400,take_profit=3, stop_loss=3))

        return pnl

        