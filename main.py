import requests

from twilio.rest import Client

account_sid = 'AC621feba4bd9c7020131942e5b71d3fc5'
auth_token = '0867ae6248f699e83f8b188e316f9c50'
appid = '6c0eafd8dee7d249c8171421df8ce568'
client = Client(account_sid, auth_token)

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = 'CJNAKO0VE7IPOMO1'
NEWS_API_KEY = 'e0d51113bfc34786a578c8667a8cb59d'


# STEP 1: Use https://www.alphavantage.co/documentation/#daily When stock price increase/decreases by 5%
# between yesterday and the day before yesterday then print("Get News"). Get yesterday's closing stock price. Hint:
# You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
stock_params ={
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_NAME,
    'apikey': STOCK_API_KEY
}


response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[1]
yesterday_closing_price = yesterday_data['4. close']

# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[2]
day_before_yesterday_closing_price = day_before_yesterday_data['4. close']

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
diference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
positive_diference = abs(diference)
# Work out the percentage difference in price between closing price yesterday and closing price the day before
# yesterday.
diff_percentage = positive_diference/float(day_before_yesterday_closing_price)*100
print(diff_percentage)
#If TODO4 percentage is greater than 5 then print("Get News").


    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

# Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
if diff_percentage > 0.2:
    news_params = {
        'apiKey': NEWS_API_KEY,
        'qInTitle': COMPANY_NAME
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_data = news_response.json()
    articles = news_data['articles']
    print(articles)
# Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
three_articles = articles[:3]
print(three_articles)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

# Create a new list of the first 3 article's headline and description using list comprehension.
news_articles_list = [f"Headline: {articles['title']}\nBrief: {articles['description']}" for articles in three_articles]
print(news_articles_list)
# Send each article as a separate message via Twilio.

if diference > 0:
    signal = '🔺'
else:
    signal = '🔻'

for messages in news_articles_list:
    print(f"{COMPANY_NAME}: {signal}{int(diff_percentage)}%\n{messages}")
    message = client.messages.create(
        body=f"{COMPANY_NAME}: {signal}{int(diff_percentage)}%\n{messages}",
        from_='+13236732896',
        to='+573157700930'
    )
    print(message.status)


#Optional Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

