import os
from typing import ByteString
import pandas as pd
import alpaca_trade_api as tradeapi
from settings import loadEnv
import threading
loadEnv("PAPER")


ws_url = 'wss://data.alpaca.markets'

conn = tradeapi.stream2.StreamConn(os.getenv("APCA_API_KEY_ID"), os.getenv("APCA_API_SECRET_KEY"), os.getenv("APCA_API_BASE_URL"),data_url=ws_url, data_stream='alpacadatav1')


# @conn.on(r'^account_updates$')
# async def on_account_updates(conn, channel, account):
#     print('account', account)

# @conn.on(r'^trade_updates$')
# async def on_trade_updates(conn, channel, trade):
#     print('trade', trade)

@conn.on(r'^AM.AAPL$')
async def on_minute_bars(conn, channel, bar):
    print('bars', bar)

def ws_start():
	conn.run(['account_updates', 'trade_updates', 'AM.AAPL'])

ws_start()

 #start WebSocket in a thread
# ws_thread = threading.Thread(target=ws_start, daemon=True)
# ws_thread.start()

