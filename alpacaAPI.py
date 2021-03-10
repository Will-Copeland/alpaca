import logging
import alpaca_trade_api as tradeapi
from settings import loadEnv


class AlpacaAPI(object):
    def __init__(self, *args):
        super(AlpacaAPI, self).__init__(*args)
        print("Initializing Alpaca API...")
        loadEnv("PAPER")

        self.api = tradeapi.REST(api_version='v2')
        return self

    def time_to_market_close(self):
        clock = self.api.get_clock()
        return (clock.next_close - clock.timestamp).total_seconds()

    def time_to_market_open(self):
        clock = self.api.get_clock()
        return (clock.next_open - clock.timestamp).total_seconds()


    def send_order(self, symbol, qty, side, type, time_in_force, order_class=None, stop_loss=None, take_profit=None, trail_price=None, trail_percent=None, extended_hours: bool = None, limit_price=None):
        try:
            print("Sending order")
            self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type=type,
                limit_price=limit_price,
                time_in_force=time_in_force,
                order_class=order_class,
                stop_loss=stop_loss,
                take_profit=take_profit,
                extended_hours=extended_hours,
                trail_price=trail_price,
                trail_percent=trail_percent,
            )
            return True
        except Exception as e:
            print("ORDER FAILED ", e)
            logging.exception(e)
            return False

    def send_bracket_limit_order(self,
                                 symbol,
                                 qty,
                                 side,
                                 stop_loss,
                                 take_profit):
        try:
            print("Sending order")
            self.send_order(
                symbol,
                qty,
                side,
                type="limit",
                time_in_force="day",
                order_class="bracket",
                stop_loss=stop_loss,
                take_profit=take_profit,
            )
        except:
            print("ORDER FAILED")




API = AlpacaAPI();