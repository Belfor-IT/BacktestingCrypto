import pprint
from typing import *
import logging

import requests


logger = logging.getLogger()


class KucoinClient:
    def __init__(self, futures: bool):

        self.futures = futures
        self.platform = "kucoin"

        if self.futures:
            self._base_url = "https://api-futures.kucoin.com"
        else:
            self._base_url = "https://api.kucoin.com"

        self.symbols = self._get_symbols()

    def _make_request(self, endpoint: str, query_parameters: Dict):

        try:
            response = requests.get(self._base_url + endpoint, params=query_parameters)
        except Exception as e:
            logger.error("Connection error while making request to %s: %s", endpoint, e)
            return None

        if response.status_code == 200:
            return response.json()
        else:
            logger.error("Error while making request to %s: %s (status code = %s)",
                         endpoint, response.json(), response.status_code)
            return None

    def _get_symbols(self) -> List[str]:

        params = dict()

        endpoint = "/api/v1/contracts/active" if self.futures else "/api/v1/symbols"
        data = self._make_request(endpoint, params)
        symbols = [x["symbol"] for x in data["data"]]

       # print(symbols)

        return symbols


    def get_historical_data(self, symbol: str, start_time: Optional[int] = None, end_time: Optional[int] = None):
            
            params = dict()
            params["symbol"] = symbol
            params["type"] = "15min"

            if start_time is not None:
                params["startAt"] = start_time
            if end_time is not None:
                params["endAt"] = end_time

            endpoint = "/api/v1/kline/query" if self.futures else "/api/v1/market/candles"
            raw_candles = self._make_request(endpoint, params)

            candles = []


            if raw_candles is not None:
                for c in raw_candles['data']:
                    candles.append((float(c[0])*1000, float(c[1]), float(c[3]), float(c[4]), float(c[2]), float(c[5]),))
                return candles
            else: 
                return None


