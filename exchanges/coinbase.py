# import logging
# import typing
# import requests
# import cbpro


# from typing import *


# logger = logging.getLogger()


# class CoinbaseClient:
#     def __init__(self):
#         self._coinbasePro = cbpro.AuthenticatedClient("c8ff0cb5cc5ea6f0c0ccf28e405d79bb","YX3oiTZoDcw6SPn0zVrSQYSZkaGhKcZBKaApbd4RDPdSAHqez/BXK387xZCiBmXArsIN1UvV2tQt6ptFyEQAFw==","pj9hw4a9fh9")
#         self.platform = "coinbase"
#         self.symbols = self._get_symbols()


#     def _get_symbols(self) -> List[str]:
#         params = dict()
#         data = self._coinbasePro.get_products()

#         symbols = [x["id"] for x in data]

#         return symbols

#     def get_historical_data(self, symbol: str, start_time: Optional[int] = None, end_time: Optional[int] = None, interval: Optional[int] = 60):
#         if interval == "1m":
#             interval = 60
#         elif interval == "5m":
#             interval = 300
#         elif interval == "1h":
#             interval = 3600
#         elif interval == "6h":
#             interval = 21600
#         elif interval == "1d":
#             interval = 86400
#         else:
#             logger.error("Invalid interval for Coinbase set to 5 min")
#             interval = 300
#         params = dict()
#         params['product_id'] = symbol
#         params['granularity'] = interval

#         if start_time is not None:
#             params["startTime"] = start_time
#         if end_time is not None:
#             params["endTime"] = end_time

#         raw_candles =  self._coinbasePro.get_product_historic_rates(params)

#         candles = []

#         print(raw_candles)

#         # if raw_candles is not None:
#         #     for c in raw_candles:
#         #         candles.append(Candle(c, interval, "coinbasePro"))
#         #         print(c)

#         if raw_candles is not None:
#             for c in raw_candles:
#                 candles.append((float(c[0]), float(c[3]), float(c[2]), float(c[1]), float(c[4]), float(c[5]),))
#             return candles
#         else: 
#             return None




