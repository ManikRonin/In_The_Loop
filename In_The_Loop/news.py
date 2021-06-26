import requests
import datetime as dt
import pandas as pd

'''
This file produces the news used in app.py
'''
# ******************* NEWS API ******************* #
NEWS_API_URL = "https://newsapi.org/v2/everything"


def new_report(symbol, my_news_api):
    """
    :param symbol
    (type: str)
    Accepts a valid Stock Symbol (Ticker) as a param for API call

    :param my_news_api
    (type: str)
    Your personal News API key

    :return: news_total_info (pandas DataFrame)
    Clean collection of the News data
    """
    today = dt.date.today()
    three_days_ago_from_today = today - dt.timedelta(days=3)

    # --------------NEWS API-------------- #

    news_parameters = {
        "apiKey": my_news_api,
        "q": symbol,
        "from": three_days_ago_from_today,
        "language": "en",
        "pageSize": 10
    }

    news_response = requests.get(url=NEWS_API_URL, params=news_parameters)
    news_response.raise_for_status()
    news = news_response.json()["articles"]

    # --------------FORM EASY TO READY DATA POINTS FOR EACH ARTICLE-------------- #

    article_total = []

    for article in news:
        current_article = {
            "Article Source": article["source"]["name"],
            "Title": article["title"],
            "Description": article["description"],
            "URL": article["url"],
            "Image": article["urlToImage"]
        }
        article_total.append(current_article)

    # --------------CREATE AN EPIC DATAFRAME FROM ALL THE DATA POINTS FOR EASY ACCESS-------------- #

    news_total_info = pd.DataFrame(article_total)
    return news_total_info
