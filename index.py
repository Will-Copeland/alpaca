from strats.sampleStrat1 import SampleStrat1
import alpaca_trade_api as tradeapi
from settings import loadEnv
import os


activeStategies = [SampleStrat1];
activeTickers = ["AAPL", "TSLA"];
utilityListeners = ["trade_updates"]
loadEnv("PAPER")

api_key = os.getenv("APCA_API_KEY_ID")
api_secret = os.getenv("APCA_API_SECRET_KEY")
base_url = 'https://paper-api.alpaca.markets'
data_url = 'wss://data.alpaca.markets'


conn = tradeapi.stream2.StreamConn(
  api_key,
  api_secret,
  base_url=base_url,
  data_url=data_url,
  data_stream='alpacadatav1',
)

for strat in activeStategies:
    strat(conn, activeTickers)


conn.run(activeTickers.extend(utilityListeners))