import backtrader as bt
import alpaca_backtrader_api
import pandas as pd
from settings import loadEnv
import os


loadEnv("PAPER")
ALPACA_KEY_ID = os.getenv("APCA_API_KEY_ID")
ALPACA_SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
ALPACA_PAPER = True


is_live = False

cerebro = bt.Cerebro()
cerebro.addstrategy(SmaCross)

store = alpaca_backtrader_api.AlpacaStore()

if is_live:
    broker = store.getbroker()  # or just alpaca_backtrader_api.AlpacaBroker()
    cerebro.setbroker(broker)
else:
    cerebro.broker.setcash(100000)
    cerebro.broker.setcommission(commission=0.0)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=20)

DataFactory = store.getdata # or use alpaca_backtrader_api.AlpacaData
if is_live:
  data0 = DataFactory(
    dataname='AAPL',
    timeframe=bt.TimeFrame.TFrame("Minutes"),
    )
else:
    data0 = DataFactory(
        dataname='AAPL',
        timeframe=bt.TimeFrame.TFrame("Minutes"),
        fromdate=pd.Timestamp('2018-11-15'),
        todate=pd.Timestamp('2018-11-17'),
        historical=True)
cerebro.adddata(data0)

cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()