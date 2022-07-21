import pandas as pd

def make_daily_close(pulled_df, tickers):
    
    # Create an empty list to hold the dictionaries for each day
    closing_data = []
    
    # Iterate through each unique timestamp to grab each stocks data
    for date in pulled_df.index.unique():
        
        # Create a dictionary to hold the timestamp, and each stocks closing price
        day_data = {}
        
        # Store the current timestamp that we are pulling data for
        day_data['Timestamp'] = date
        
        # Iterate through the tickers for that day, and grab each ones stock price
        for stock in tickers:
            day_data[stock] = pulled_df.loc[(pulled_df.index == date) & (pulled_df['symbol'] == stock), 'close'].item()
        
        # Append the current timestamps data to the list
        closing_data.append(day_data)
        
    # Create a dataframe from the list of closing price dictionaries
    cleaned_data = pd.DataFrame(closing_data)
    
    # Return the dataframe
    return cleaned_data