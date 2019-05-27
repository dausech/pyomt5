from enum import Enum


class MT5TimeFrame(Enum):
    """ 
    Metatrader 5 dataframes
    """
    M1 = 1  # 1 minute
    M5 = 5  # 5 minutes
    M15 = 15  # 15 minutes
    M30 = 30  # 30 minutes
    Hourly = 60  # 1 hourly
    Daily = 1440  # Daily
    Weekly = 10080  # Weekly
    Montly = 43200  # Monthly
