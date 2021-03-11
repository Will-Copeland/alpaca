from strategies.CriticalTradingMA import CritialTradingMA
from Sizers.LongOnly import LongOnly
from strategies.donchainChannel import MyStrategy
import alpaca_backtrader_api as Alpaca
import backtrader as bt
import pytz
from datetime import datetime
from settings import loadEnv
import os


loadEnv("PAPER")
ALPACA_KEY_ID = os.getenv("APCA_API_KEY_ID")
ALPACA_SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
ALPACA_PAPER = True

fromdate = datetime(2020, 1, 1)
todate = datetime(2020, 3, 1)

tickers = ['TSLA']
timeframes = {
    # '15Days': 15,
    'daily': 1
}

cerebro = bt.Cerebro()
cerebro.addstrategy(CritialTradingMA)
cerebro.addsizer(LongOnly)
cerebro.addsizer(bt.sizers.PercentSizer)
# cerebro.broker.setcash(100000)
# cerebro.broker.setcommission(commission=0.0)

print("cerebro init")
store = Alpaca.AlpacaStore()

print("store init", ALPACA_PAPER)

if not ALPACA_PAPER:
    print(f"LIVE TRADING")
    broker = store.getbroker()
    cerebro.setbroker(broker)

print("run tick")
for ticker in tickers:
    for timeframe, minutes in timeframes.items():
        print(f'Adding ticker {ticker} using {timeframe} timeframe at {minutes} minutes.')
        DataFactory = Alpaca.AlpacaData
        d = DataFactory(
                dataname=ticker,
                timeframe=bt.TimeFrame.Days,
                historical=False)

        cerebro.adddata(d)


cerebro.run()
print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
cerebro.plot(style='candlestick', barup='green', bardown='red')
