import os
import requests
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
import questionary 


def api_call():
    load_dotenv()
    
    alpaca_api = os.getenv("ALPACA_API_KEY")
    alpaca_secret = os.getenv("ALPACA_SECRET_KEY")
    
    alpaca = tradeapi.REST(
        alpaca_api,
        alpaca_secret,
        api_version="v2"
    )
    
    return alpaca




