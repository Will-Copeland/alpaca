from datetime import datetime

from backtrader import position
from indicators.HighHighLowLow import HighHighLowLow
from indicators.DonchainChannels import DonchianChannels
import backtrader as bt


class CritialTradingMA(bt.Strategy):
    params = dict(
        period=5,
        lookback=-5
    )

    lines = ('hi', 'lo')

    def __init__(self):
        self.orefs = None
        self.inds = {}
        self.hi = bt.ind.Highest(self.data, period=5, subplot=False)
        self.lo = bt.ind.Lowest(self.data, period=5, subplot=False)
        self.maxPos = 0

    def next(self):
        if self.position.size > self.maxPos:
          self.maxPos = self.position.size
          # print(self.getpositions(self.data))

        if self.data[0] < self.hi[0]:
            # print(self.position.size)
            if not self.position.size:
              print("BUY")
              self.buy_bracket(data=s)
              self.orefs
        elif self.data[0] > self.lo[0]:
            if self.position.size:
              print("SELL")
              self.sell()


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print(f'{str(dt.isoformat())}: {txt}')

    def notify_trade(self, trade):
        if not trade.size:
            print(f'Trade PNL: ${trade.pnlcomm:.2f}')

    def notify_order(self, order):
        print(order)
        # self.log(f'Order - {order.getordername()} {order.ordtypename()} {order.getstatusname()} for {order.size} shares @ ${order.price:.2f}')

        if not order.alive() and order.ref in self.orefs:
            self.orefs.remove(order.ref)
