# This is the example code from the repo's README
import alpaca_backtrader_api
import backtrader as bt
from datetime import datetime
from settings import loadEnv
import os

# loadEnv("PAPER")

# Your credentials here
# ALPACA_KEY_ID = os.getenv("APCA_API_KEY_ID")
# ALPACA_SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
APCA_API_BASE_URL="https://paper-api.alpaca.markets"
ALPACA_KEY_ID="PKUJ260EM0RJROT06RRI"
ALPACA_SECRET_KEY="284ebJOp702w8dc7V29CrD5zsxhfQaNjktV0sIe0"

"""
You have 3 options:
 - backtest (IS_BACKTEST=True, IS_LIVE=False)
 - paper trade (IS_BACKTEST=False, IS_LIVE=False)
 - live trade (IS_BACKTEST=False, IS_LIVE=True)
"""
IS_BACKTEST = True
IS_LIVE = False
symbol = "AAPL"
USE_POLYGON = False


class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)

    store = alpaca_backtrader_api.AlpacaStore(
        key_id=ALPACA_KEY_ID,
        secret_key=ALPACA_SECRET_KEY,
        paper=not IS_LIVE,
        usePolygon=USE_POLYGON
    )

    DataFactory = store.getdata  # or use alpaca_backtrader_api.AlpacaData
    if IS_BACKTEST:
        data0 = DataFactory(dataname=symbol, historical=True,
                            fromdate=datetime(
                                2015, 1, 1), timeframe=bt.TimeFrame.Days)
    else:
        data0 = DataFactory(dataname=symbol,
                            historical=False,
                            timeframe=bt.TimeFrame.Days)
        # or just alpaca_backtrader_api.AlpacaBroker()
        broker = store.getbroker()
        cerebro.setbroker(broker)
    cerebro.adddata(data0)

    print('Starting Portfolio Value: {}'.format(cerebro.broker.getvalue()))
    cerebro.run()
    print('Final Portfolio Value: {}'.format(cerebro.broker.getvalue()))
    cerebro.plot()