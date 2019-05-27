from pyomt5.api import MT5TimeFrame
from pyomt5.stock import StockPriceHistory

c = StockPriceHistory()

data = c.get_price_history_as_df('PETR4', MT5TimeFrame.Daily)
print(data.dtypes)
