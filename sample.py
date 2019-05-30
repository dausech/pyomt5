from datetime import datetime
from pyomt5.api import MT5TimeFrame
from pyomt5.stock import StockPriceHistory

c = StockPriceHistory()

start_date = datetime(2019, 1, 1)
end_date = datetime(2019, 5, 2)
data = c.get_price_from(symbol='PETR4',
                        from_date=start_date,
                        to_date=end_date,
                        timeframe=MT5TimeFrame.Daily)

print(data)

start_date = datetime(2019, 1, 2, 10, 0)
end_date = datetime(2019, 1, 2, 12, 0, 0)
data = c.get_price_from(symbol='PETR4',
                        from_date=start_date,
                        to_date=end_date,
                        timeframe=MT5TimeFrame.M5)

print(data)