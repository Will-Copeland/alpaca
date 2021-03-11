from bt_example import DataFactory
from datetime import datetime
import backtrader as bt



class MyStrategy(bt.Strategy):
    def __init__(self):
        self.myind = DonchianChannels();

    def next(self):
        if self.data[0] > self.myind.dch[0]:
            self.buy()
        elif self.data[0] < self.myind.dcl[0]:
            self.sell()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MyStrategy)
    cerebro.broker.setcash(5000.0)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=20)


    data = bt.feeds.YahooFinanceData(dataname='AAPL',
                                     fromdate=datetime(2017, 1, 1),
                                     todate=datetime(2017, 12, 31))
    cerebro.adddata(data)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()