pyOMT5 - Python Open MetaTrader 5
===================================

Python module to request data from MetaTrader 5

To get started:
- create a new directory called pyOMT5 inside your MT5 Scrips folder. Ex: C:\Users\MyUser\AppData\Roaming\MetaQuotes\Terminal\83D4764E0403A8685E84D6FCAB361AAB\MQL5\Scripts\pyOMT5
- copy the files pyOMT5Server.mq5 and pyOMT5Server.ex5 from util directory to this new directory and compile it using MetaEditor if necessary.
- download DLL files according your OS (32|64 Bits) from https://github.com/dingmaotu/mql-zmq/
-   run pyOMT5Server as a expert. Remember to have enabled auto trading option and allow DLLs imports when asked.

This module provides data in pandas representation because we believe that whether in finance, scientific fields, or data science, a familiarity with Pandas is known by everyone.

This library uses ZeroMQ and create a internal tcp server on MetaTrader, with the purpose of exchange data with MT5.


Install
---------
To install the package use:
``` {.sourceCode .bash}
pip install pyOMT5
```

If you want to install from source, then use:
``` {.sourceCode .bash}
git clone https://github.com/paulorodriguesxv/pyOMT5.git
pip install -e pyOMT5
```

Usage
-------
``` {.sourceCode .python}

from pyomt5.api import MT5TimeFrame
from pyomt5.stock import StockPriceHistory


c = StockPriceHistory()
data = c.get_price_history_as_df('PETR4', MT5TimeFrame.Daily)
print(data)

```

Contributing
-------------
Contributing is always welcome, so, feel free to getting in touch and contribute.

TODOs
-------------
-   Add test for library.
-   Create sphinx docs
-   Create travis
-   Extend Api
  
Star if you like it.
---------------------
If you like or use this project, consider showing your support by starring it.
