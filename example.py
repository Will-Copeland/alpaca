
import logging
from time import sleep
import os

import alpaca_trade_api as tradeapi
import pandas as pd
from settings import loadEnv


loadEnv("PAPER")
# init
logging.basicConfig(
  filename='errlog.log',
  level=logging.WARNING,
  format='%(asctime)s:%(levelname)s:%(message)s',
)
api_key = os.getenv("APCA_API_KEY_ID")
api_secret = os.getenv("APCA_API_SECRET_KEY")
base_url = 'https://paper-api.alpaca.markets'
data_url = 'wss://data.alpaca.markets'


# instantiate REST API
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# account = api.get_account()
orders = api.list_orders()
pos = api.list_positions()
clock = api.get_clock()

# ord = api.get_order_by_client_order_id("0009")

# print("0009", ord)
print(orders, 'pos', pos, clock)

# init WebSocket clock = api.get_clock()
conn = tradeapi.stream2.StreamConn(
  api_key,
  api_secret,
  base_url=base_url,
  data_url=data_url,
  data_stream='alpacadatav1',
)

def time_to_market_close():
  clock = api.get_clock()
  return (clock.next_close - clock.timestamp).total_seconds()


def wait_for_market_open():
  clock = api.get_clock()
  if not clock.is_open:
    time_to_open = (clock.next_open - clock.timestamp).total_seconds()
    sleep(round(time_to_open))


def set_trade_params(df):
  high = df.high.tail(10).max()
  low = df.low.tail(10).min()
  print("high", high, "low", low)
  return {
    'high': high,
    'low': low,
    'trade_taken': False,
  }



def forceOrd():
  print("send")
  try:
    api.submit_order(
      symbol='AAPL',
      qty=100,
      side="buy",
      type='market',
      time_in_force='fok',
      order_class='simple',
      # stop_loss=dict(stop_price=str(sl)),
      # take_profit=dict(limit_price=str(tp)),
      )
  except:
    logging.exception("order not sent")

def send_order(direction, bar):

  if time_to_market_close() > 120:
    print(f'sent {direction} trade')
    range_size = trade_params['high'] - trade_params['low']

    if direction == 'buy':
      sl = bar.high - range_size
      tp = bar.high + range_size
      print(sl, tp)
    elif direction == 'sell':
      sl = bar.low + range_size
      tp = bar.low - range_size
      print(sl, tp)

    print("SEnd TRADE")
    # forceOrd()
    try:
      resp = api.submit_order(
        symbol='AAPL',
        qty=100,
        side="buy",
        type='market',
        time_in_force='fok',
        order_class='simple',
        # stop_loss=dict(stop_price=str(sl)),
        # take_profit=dict(limit_price=str(tp)),
        )
      print("Buy ord sent!", resp)
      return True
    except:
      print("ORDER NOT SENT")
      logging.exception("ORDER NOT SENT")
      return False

  wait_for_market_open()
  return False


@conn.on(r'^AM.AAPL$')
async def on_minute_bars(conn, channel, bar):
  print(bar)
  if isinstance(candlesticks.df, pd.DataFrame):
    ts = pd.to_datetime(bar.timestamp, unit='ms')
    candlesticks.df.loc[ts] = [bar.open, bar.high, bar.low, bar.close, bar.volume]
    print("here")
    res = send_order('buy', bar)

  if not trade_params['trade_taken']:
    if bar.high > trade_params['high']:
      trade_params['trade_taken'] = send_order('buy', bar)

    elif bar.low < trade_params['low']:
      trade_params['trade_taken'] = send_order('sell', bar)

  if time_to_market_close() > 120:
    wait_for_market_open()


@conn.on(r'^trade_updates$')
async def on_trade_updates(conn, channel, trade):
  print(trade)
  if trade.order['order_type'] != 'market' and trade.order['filled_qty'] == '100':
    # trade closed - look for new trade
    trade_params = set_trade_params(candlesticks.df.AAPL)


candlesticks = api.get_barset('AAPL', 'minute', limit=10)
trade_params = set_trade_params(candlesticks.df.AAPL)
conn.run(['AM.AAPL', 'trade_updates'])