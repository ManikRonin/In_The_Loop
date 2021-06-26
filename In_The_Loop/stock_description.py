import requests
import pandas

'''
This file produces the descriptions used in app.py
'''


def company(symbol, my_financial_mp):
    """
    :param symbol
    (type: str)
    Accepts a valid Stock Symbol (Ticker) as a param for API call

    :param my_financial_mp
    (type:str)
    You personal FinancialModellingPrep API key to access the data

    :return df_company (pandas DataFrame)
    Set of useful information and ratios for a quick company overview

    “Data provided by Financial Modeling Prep”
    https://financialmodelingprep.com/developer/docs/
    """

    # Get part 1 of data
    url = f'https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={my_financial_mp}'
    response = requests.get(url)
    co_profile = response.json()[0]

    # Get part 2 of data
    url = f'https://financialmodelingprep.com/api/v3/ratios-ttm/{symbol}?apikey={my_financial_mp}'
    response = requests.get(url)
    co_ratios = response.json()[0]

    # Take relevant points from both datasets and put them together in a clean dict
    company_overview = [
        {'Category': 'Name', 'Current': co_profile['companyName']},
        {'Category': 'Symbol', 'Current': co_profile['symbol']},
        {'Category': 'Current Price ($USD)', 'Current': co_profile['price']},
        {'Category': 'PE Ratio', 'Current': round(co_ratios['peRatioTTM'], 3)},
        {'Category': 'PEG Ratio', 'Current': round(co_ratios['pegRatioTTM'], 3)},
        {'Category': 'Pretax Profit Margin (%)', 'Current': round(co_ratios['pretaxProfitMarginTTM'] * 100, 3)},
        {'Category': 'Net Profit Margin (%)', 'Current': round(co_ratios['netProfitMarginTTM'] * 100, 3)},
        {'Category': 'Exchange', 'Current': co_profile['exchangeShortName']},
        {'Category': 'Industry', 'Current': co_profile['industry']},
        {'Category': 'Sector', 'Current': co_profile['sector']},
        {'Category': 'Website', 'Current': co_profile['website']},
        {'Category': 'Ceo', 'Current': co_profile['ceo']},
        {'Category': 'Location', 'Current': co_profile['country']},
        {'Category': 'Description', 'Current': str(co_profile['description'])}
    ]

    df_company = pandas.DataFrame(company_overview)

    return df_company
