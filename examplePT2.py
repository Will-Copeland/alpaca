from strategies.RSIStack import RSIStack
import alpaca_backtrader_api as alpaca
import backtrader as bt
import pytz
from datetime import datetime
from settings import loadEnv
import os
import pandas as pd
from strategies.CriticalTradingMA import CritialTradingMA
from Sizers.LongOnly import LongOnly



loadEnv("PAPER")

ALPACA_KEY_ID = os.getenv("APCA_API_KEY_ID")
ALPACA_SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
ALPACA_PAPER = True

IS_BACKTEST = False

fromdate = pd.Timestamp(2019,5,1)
todate = pd.Timestamp(2020,8,17)
timezone = pytz.timezone('US/Eastern')

tickers = ['VTI']
timeframes = {
    '15Min':1,
    # '30Min':30,
    # '1H':60,
}
lentimeframes = len(timeframes)


cerebro = bt.Cerebro()
cerebro.addstrategy(RSIStack)
# cerebro.addsizer(LongOnly)
cerebro.addsizer(bt.sizers.PercentSizer)
cerebro.broker.setcash(100000)
cerebro.broker.setcommission(commission=0.0)

store = alpaca.AlpacaStore(
    key_id=ALPACA_KEY_ID,
    secret_key=ALPACA_SECRET_KEY,
    paper= False
)

if not IS_BACKTEST:
  print(f"LIVE TRADING")
  broker = store.getbroker()
  cerebro.setbroker(broker)



DataFactory = store.getdata

for ticker in tickers:
    for timeframe, minutes in timeframes.items():
        print(f'Adding ticker {ticker} using {timeframe} timeframe at {minutes} minutes.')

        d = DataFactory(
            dataname=ticker,
            timeframe=bt.TimeFrame.Days,
            # compression=minutes,
            # fromdate=fromdate,
            # todate=todate,
            historical=False)

        cerebro.adddata(d)

cerebro.run()
print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
cerebro.plot(style='candlestick', barup='green', bardown='red')