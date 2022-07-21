import os
import requests
import json
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi
import streamlit as st
import copy
import matplotlib.pyplot as plt
from api_caller import api_call
from dotenv import load_dotenv
from make_close_price import make_daily_close
from find_portfolio_weights import portfolio_weights
from find_portfolio_weights import portfolio_total
from monte_carlo_df import create_simulation_df
from MCForecastTools import MCSimulation


st.title("Portfolio Forecasting App")
st.sidebar.markdown('''
Use the following instructions to correctly format your portfolio data for the simulation:

- The app takes a single CSV file. To start, open an excel workbook and create two columns: 'Ticker' and 'Quantity' 
    - Add the company ticker to the ticker column
    - Add the quantity to the quantity column
    - Save the excel book as a CSV file
    - Drag and drop file into app to begin simulation

    ''')

portfolio_data = st.file_uploader("Upload Portfolio Information Here:")
if portfolio_data is not None: 
    member_df = pd.read_csv(portfolio_data)
    tickers = list(member_df['Ticker'].unique()) 

    initial_price_date = st.date_input("Please enter a start date for historical data.")
    end_price_date = st.date_input("Please enter an end date for historical data.")
    start_date = pd.Timestamp(str(initial_price_date), tz="America/New_York").isoformat()
    end_date = pd.Timestamp(str(end_price_date), tz="America/New_York").isoformat()
    timeframe = "1Day"

    alpaca_data = api_call()

    historical_data = alpaca_data.get_bars(
        tickers,
        timeframe, 
        start = start_date,
        end = end_date
    ).df

   
    cleaned_df = make_daily_close(historical_data, tickers)
  
    weight = portfolio_weights(cleaned_df, member_df, tickers)
    
    portfolio_value = round(portfolio_total(cleaned_df, member_df), 2)
    
    simulation_df = create_simulation_df(historical_data)
    
    
    simulation_length = int(st.number_input("How many year do you want to simulate?", min_value=1))
    
    st.metric("Starting Portfolio Value", f"${portfolio_value:,}")
    
    if st.button("Press here to start simulation"):
    
        MC_sim = MCSimulation(
        portfolio_data = simulation_df,
        weights = weight,
        num_simulation = 150,
        num_trading_days = 252 * simulation_length)

        MC_sim_daily_return = MC_sim.portfolio_data.head()

        MC_sim_data = MC_sim.calc_cumulative_return()
        
        MC_summary = MC_sim.summarize_cumulative_return()
       
        MC_lower = round(MC_summary[8] * portfolio_value, 2)
        
        MC_upper = round(MC_summary[9] * portfolio_value, 2)

        upper_net = round(MC_upper - portfolio_value, 2)

        lower_net = round(MC_lower - portfolio_value, 2)
        
       
        st.metric("Max Gain", f"${upper_net:,}", delta_color="normal")
        st.metric("Max Loss", f"${lower_net:,}", delta_color="normal")
        st.write(f"With a 95% confidence interval, your starting portfolio value of {portfolio_value:,} ranges from {MC_lower:,} to {MC_upper:,} over {simulation_length} year(s).")
          
       
   
        
  
    

    


    
    

    
   
    
    


        
    