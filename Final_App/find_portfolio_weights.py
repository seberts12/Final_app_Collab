import pandas as pd
import numpy as np


def portfolio_weights(clean_data, portfolio_positions, tickers):
    x = clean_data.iloc[-1,1:].to_list()
    y = portfolio_positions["Quantity"].to_list()
    total = np.dot(x, y)
    ticker_weights = {}
    for ticker in tickers:
        stock_price = clean_data[ticker].to_list()[-1]
        stock_quantity = portfolio_positions.loc[portfolio_positions['Ticker'] == ticker, 'Quantity'].item()
        stock_position = stock_price * stock_quantity
        ticker_weights[ticker] = round(stock_position / total, 2)
    weight = []
    for value in ticker_weights.values():
        weight.append(value)
    return weight


def portfolio_total(clean_data, portfolio_positions):
    x = clean_data.iloc[-1,1:].to_list()
    y = portfolio_positions["Quantity"].to_list()
    total = np.dot(x, y)
    return total