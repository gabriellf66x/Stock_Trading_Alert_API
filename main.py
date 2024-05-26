import os
import requests
from datetime import datetime, timedelta
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

VIRTUAL_TWILIO_NUMBER = "Twilio number"
VERIFIED_NUMBER = "Phone number verified with Twilio"

STOCK_API_KEY = "API KEY FROM ALPHAVANTAGE"
NEWS_API_KEY = "API KEY FROM NEWSAPI"
TWILIO_SID = "TWILIO ACCOUNT SID"
TWILIO_AUTH_TOKEN = "TWILIO AUTH TOKEN"

Stock_Endpoint = ("https://www.alphavantage.co/query")
News_Endpoint = ('https://newsapi.org/v2/everything')

# yesterday's closing price
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}

response = requests.get(Stock_Endpoint, params=stock_params)
data = response.json()
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

# day before yesterday closing price
day_before_yesterday = data_list[1]
day_before_yesterday_closing = day_before_yesterday["4. close"]

# positive difference
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# work out percentage diference
diff_percent = round((difference / float(yesterday_closing_price)) * 100)

if abs(diff_percent) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(News_Endpoint, params=news_params)
    articles = news_response.json()['articles']
    three_articles = articles[:3]

    # first 3 articles headline and description
    formatted_articles = [f"{STOCK}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    # separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )


