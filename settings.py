from dotenv import load_dotenv, find_dotenv
from enum import Enum

TradeModeMap = {
  "PAPER": ".env-paper",
  "LIVE" : ".env-live"
}

def loadEnv(tradeMode):
  load_dotenv(find_dotenv(TradeModeMap[tradeMode]))