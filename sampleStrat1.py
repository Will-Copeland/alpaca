from alpacaAPI import API
import pandas as pd



class SampleStrat1(object):
    def __init__(self, conn, tickers):
        super(SampleStrat1, self).__init__()
        self.candlesticks = initialBars;
        self.trade_params = self.set_trade_params(self.candlesticks)
        self.api = API


    def get_barsets(self, tickers):
        for ticker in tickers:
            self.api.api.get_barset(ticker, 'minute', limit=10)


    def set_trade_params(self, df):
        high = df.high.tail(10).max()
        low = df.low.tail(10).min()
        print("high", high, "low", low)
        self.trade_params = {
            'high': high,
            'low': low,
            'trade_taken': False,
        }

    def getOrderParams(self, direction, bar):
        range_size = self.trade_params['high'] - self.trade_params['low']

        if direction == 'buy':
            sl = bar.high - range_size
            tp = bar.high + range_size
            print(sl, tp)
            return [sl, tp]
        elif direction == 'sell':
            sl = bar.low + range_size
            tp = bar.low - range_size
            print(sl, tp)
            return [sl, tp]


    def send_order(self, direction, bar):
        [sl, tp] = self.getOrderParams(direction=direction, bar=bar)

        try:
            self.api.send_order(
            symbol='AAPL',
            qty=100,
            side="buy",
            type='market',
            time_in_force='fok',
            order_class='bracket',
            stop_loss=dict(stop_price=str(sl)),
            take_profit=dict(limit_price=str(tp)),
            )
        except Exception as e:
            print("SAMPLE STRAT 1 FAILED TO PLACE ORDER ", e)


    def insertBar(self, bar):
        if isinstance(self.candlesticks.df, pd.DataFrame):
            ts = pd.to_datetime(bar.timestamp, unit='ms')
            self.candlesticks.df.loc[ts] = [bar.open, bar.high, bar.low, bar.close, bar.volume]


    def onData(self, conn, channel, bar):
        self.insertBar(bar)

        if not self.trade_params['trade_taken']:
            if bar.high > self.trade_params['high']:
                self.trade_params['trade_taken'] = self.send_order('buy', bar)

            elif bar.low < self.trade_params['low']:
                self.trade_params['trade_taken'] = self.send_order('sell', bar)
