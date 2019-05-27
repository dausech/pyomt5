import time
import logging
import pandas as pd
from datetime import datetime, timedelta
from pyomt5.api import MT5TimeFrame
from pyomt5.api import MetatraderCom, ConnectionTimeoutError

log = logging.getLogger(__name__)


class StockPriceHistory():
    def __init__(self, use_cache=False):
        self.use_cache = use_cache
        self.price_cache = dict()

    def get_price_history(self,
                          symbol: str,
                          timeframe: MT5TimeFrame,
                          periods=250) -> list:
        """ Get prices from history data
            Args:
                symbol (str): symbol of stock
                timeframe (MT5TimeFrame): interval between each price-time
                periods: amount of data that'll be returned
            Returns:
                list: a list with all data in the OHLC format 
                Ex:
                    [{'date': '2018.09.20 00:00', 'open': ' 19.5600', 'low': '19.0700', 'high': '19.6400', 'close':
                     '19.1800', 'volume': '56002300'}]
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(minutes=timeframe.value * periods)

        c = MetatraderCom()
        nRetry = 0
        price_history = None
        while nRetry < 5:
            try:

                if self.use_cache and (symbol in self.price_cache):
                    log.debug(f"Getting data for {symbol} [using cache]")
                    return self.price_cache[symbol]

                log.debug(f"Getting data for {symbol}")
                price_history = c.get_historical(symbol, timeframe.value,
                                                 start_date, end_date)

                self.price_cache[symbol] = price_history
                return price_history
            except ConnectionTimeoutError:
                nRetry += 1
                log.debug(
                    f"Connection Failed. Waiting for reconnection.. Retry #{nRetry}"
                )
                time.sleep(0.5)

        return price_history

    def _convert_to_dataframe(self, data):
        df = pd.DataFrame.from_dict(data)

        df.close = pd.to_numeric(df.close)
        df.open = pd.to_numeric(df.open)
        df.low = pd.to_numeric(df.low)
        df.high = pd.to_numeric(df.high)
        df.volume = pd.to_numeric(df.volume)
        df.date = pd.to_datetime(df.date,
                                 format='%Y.%m.%d %H:%M',
                                 errors='ignore')

        return df

    def get_price_history_as_df(self, symbol, timeframe, periods=250):
        """ Get prices from history data and return it 
            in a pandas DataFrame format
            Args:
                symbol (str): symbol of stock
                timeframe (MT5TimeFrame): interval between each price-time
                periods: amount of data that'll be returned
            Returns:
                list: a list with all data in the OHLC format 
                Ex:
                                index  close   high    low   open     volume
                symbol date
                PETR4  2018-09-20    163  19.18  19.64  19.07  19.56   56002300
                       2018-09-21    162  19.44  19.60  19.26  19.45   58278000
        """
        data = self.get_price_history(symbol, timeframe, periods)

        if data is None:
            return pd.DataFrame()

        df = self._convert_to_dataframe(data)

        df['symbol'] = symbol

        return df.reset_index().sort_values(by=["symbol", "date"],
                                            ascending=True).set_index(
                                                ["symbol", "date"])
