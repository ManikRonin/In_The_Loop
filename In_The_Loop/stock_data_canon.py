import requests
import pandas as pd

'''
This file produces the data used in stock_graphs.py
'''

# ******************* INTRADAILY DATA ******************* #
def presentation_daily_data(symbol, my_alpha_vantage):
    """
    :param symbol
    (type: str)
    Accepts a valid Stock Symbol (Ticker) as a param for API call

    :param my_alpha_vantage
    (type:str)
    You personal AlphaVantage API key to access the data

    :return: daily_data (pandas DataFrame)
    Data used by function 'presentation_daily_line_graph()'
    in stock_graphs.py file
    """
    stock_endpoint = "https://www.alphavantage.co/query"

    parameters = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '30min',
        'outputsize': 'compact',
        'apikey': my_alpha_vantage,
    }

    response = requests.get(url=stock_endpoint, params=parameters)
    response.raise_for_status()
    stock_intradaily = response.json()['Time Series (30min)']

    # Clean Up
    raw_daily_data = pd.DataFrame(stock_intradaily)
    daily_data = raw_daily_data.T
    daily_data.reset_index(level=0, inplace=True)
    daily_data.rename(columns={
        'index': 'DATE/TIME',
        '1. open': 'OPEN',
        '2. high': 'HIGH',
        '3. low': 'LOW',
        '4. close': 'CLOSE',
        '5. volume': 'VOLUME'
    },
        inplace=True)
    daily_data['DATE/TIME'] = pd.to_datetime(daily_data['DATE/TIME'])
    daily_data = daily_data[::-1]
    daily_data = daily_data.tail(-69)
    daily_data = daily_data.reset_index(drop=True)

    return daily_data


def presentation_weekly_data(symbol, my_alpha_vantage):
    """
    :param symbol
    (type: str)
    Accepts a valid Stock Symbol (Ticker) as a param for API call

    :param my_alpha_vantage
    (type:str)
    You personal AlphaVantage API key to access the data

    :return: weekly_data (pandas DataFrame)
    data used by function 'presentation_weekly_line_graph():' & 'presentation_daily_candle_graph()'
    in stock_graphs.py file
    """
    stock_endpoint = "https://www.alphavantage.co/query"

    parameters = {
        'function': 'TIME_SERIES_WEEKLY',
        'symbol': symbol,
        'apikey': my_alpha_vantage
    }

    response = requests.get(url=stock_endpoint, params=parameters)
    response.raise_for_status()
    stock_weekly = response.json()['Weekly Time Series']

    # Clean Up
    raw_weekly_data = pd.DataFrame(stock_weekly)
    weekly_data = raw_weekly_data.T
    weekly_data.reset_index(level=0, inplace=True)
    weekly_data.rename(columns={
        'index': 'DATE',
        '1. open': 'OPEN',
        '2. high': 'HIGH',
        '3. low': 'LOW',
        '4. close': 'CLOSE',
        '5. volume': 'VOLUME'
    },
        inplace=True)
    weekly_data['DATE'] = pd.to_datetime(weekly_data['DATE'])
    weekly_data = weekly_data[::-1]
    weekly_data = weekly_data.reset_index(drop=True)
    cols = weekly_data.columns.drop('DATE')
    weekly_data[cols] = weekly_data[cols].apply(pd.to_numeric)

    return weekly_data

