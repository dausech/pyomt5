import logging
import zmq
from .timeframe import MT5TimeFrame

log = logging.getLogger(__name__)

DATA_NOT_FOUND = 'NO DATA'


class DataNotFoundError(Exception):
    pass


class ConnectionTimeoutError(Exception):
    pass


class MetatraderCom():
    def __remote_send(self, socket, data):
        try:
            socket.send_string(data)
            msg = socket.recv_string()
            return (msg)
        except zmq.Again:
            log.debug("Waiting for PUSH from MetaTrader 5..")

    def __get_socket(self):
        context = zmq.Context()

        # Create REQ Socket
        reqSocket = context.socket(zmq.REQ)
        reqSocket.setsockopt(zmq.RCVTIMEO, 500)
        reqSocket.connect("tcp://localhost:5555")

        return reqSocket

    def get_historical(self, symbol: str, timeframe: MT5TimeFrame, start,
                       end) -> list:
        """ Get prices from Metatrader 5
            Args:
                symbol (str): symbol of stock
                timeframe (MT5TimeFrame): interval between each price-time
                start: start datetime of period
                end:   end datetime of period
            Returns:
                list: a list with all data in the OHLC format
                Ex:
                    [{'date': '2018.09.20 00:00', 'open': ' 19.5600',
                     'low': '19.0700', 'high': '19.6400', 'close':
                     '19.1800', 'volume': '56002300'}]

            Usage:
                start_date = datetime(year=2019, month=4, day=1,
                                      hour=10, minute=0, second=0)
                end_date = datetime(year=2019, month=4, day=3,
                                       hour=18, minute=0, second=0)

                c = MetatraderCom()
                c.get_historical('PETR4', M15, start_date, end_date)
        """
        reqSocket = self.__get_socket()

        start_date = start.strftime("%Y.%m.%d %H:%M:%S")
        end_date = end.strftime("%Y.%m.%d %H:%M:%S")
        data = self.__remote_send(
            reqSocket, f"DATA|{symbol}|{timeframe}|{start_date}|{end_date}")

        if data is None:
            reqSocket.close(100)
            raise ConnectionTimeoutError()

        if data == DATA_NOT_FOUND:
            raise DataNotFoundError()

        results = []
        for item in data.split('|'):
            splited_item = item.split(",")
            if len(splited_item) > 1:
                vdate, vopen, vlow, vhigh, \
                    vclose, vtick, vvolume = splited_item

            results.append(
                dict(date=vdate,
                     open=vopen,
                     low=vlow,
                     high=vhigh,
                     close=vclose,
                     volume=vvolume))
        return results[:-1]
