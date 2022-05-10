import logging
import time

from exchanges.binance import BinanceClient
from exchanges.ftx import FtxClient
from exchanges.kucoin import KucoinClient
from exchanges.coinbase import CoinbaseClient
from data_collector import collect_all

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s %(levelname)s :: %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler("info.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


if __name__ == "__main__":

    mode = input("Choose the program mode (data / backtest / optimize): ").lower()

    while True:
        exchange = input("Choose an exchange: ").lower()
        if exchange in ["ftx", "binance", "kucoin", "coinbase"]:
            break

    if exchange == "binance":
        client = BinanceClient(True)
        #print(client.get_historical_data("BTCUSDT"))
    elif exchange == "ftx":
        client = FtxClient()  
    elif exchange == "kucoin":
        client = KucoinClient(False)
    elif exchange == "coinbase":
        client = CoinbaseClient()
    
        

    while True:
        symbol = input("Choose a symbol: ").upper()
        if symbol in client.symbols:
            break
    
    if mode == "data":
        collect_all(client, exchange, symbol)