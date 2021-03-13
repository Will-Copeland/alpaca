import backtrader as bt


class Highest(bt.Indicator):

    plotlines = dict(
        dcm=dict(ls='--'),  # dashed line
    )

    def __init__(self, period=5):
        self.addminperiod(self.params.period)
        self.history = []
        highestHighOfPeriod = bt.ind.Highest(
            self.data, period=period, plot=True, subplot=False)
        print(highestHighOfPeriod)
        self.highest = highestHighOfPeriod
        self.lines = ('Highest')


