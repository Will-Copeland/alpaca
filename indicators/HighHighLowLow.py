import backtrader as bt


class HighHighLowLow(bt.Indicator):


  alias = ('5DMA', 'FiveDayMovingAverage');

  lines = ('maH', 'maL')

  params = dict(
    period=5,
  )
  plotlines = dict(
      # dcm=dict(ls='--'),  # dashed line
      maH=dict(ls='--'),  # use same color as prev line (dcm)
      maL=dict(_samecolor=True),  # use same color as prev line (dch)
  )

  def __init__(self):
    hiHi, loLo = bt.ind.Highest(self.data, period=self.p.period, plot=True, subplot=False), bt.ind.Lowest(self.data, period=self.p.period, plot=True, subplot=False)
    print(hiHi, loLo)
    self.maH = hiHi
    self.maL = loLo
