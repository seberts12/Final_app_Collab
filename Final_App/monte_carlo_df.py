import os
import requests
import json
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi
import streamlit as st
import copy 
from api_caller import api_call
from dotenv import load_dotenv
from make_close_price import make_daily_close
from find_portfolio_weights import portfolio_weights
from MCForecastTools import MCSimulation


def create_simulation_df(df_portfolio):
    test = {}
    for ticker in df_portfolio['symbol'].unique():
        test[ticker] = copy.deepcopy(df_portfolio.loc[df_portfolio['symbol'] == ticker])
        test[ticker].drop(columns = ['symbol'], inplace = True)
    testing_df = pd.concat([test[key] for key in test.keys()], axis=1, keys=test.keys())
    return testing_df