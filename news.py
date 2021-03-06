import requests
import datetime
import responses

API_KEY = 'c10aaad5b172490b9ff1b954d6cec496'


def get_top_news():
    top_url = 'http://newsapi.org/v2/top-headlines?country=au&from=' + get_date() + '&apiKey=' + API_KEY
    get_news(top_url)


def get_news_about(topic):
    question_url = 'http://newsapi.org/v2/everything?qInTitle=' + topic + '&sortBy=relevancy&language=en&from=' + get_date() + '&apiKey=' + API_KEY
    get_news(question_url)


def get_news(url):
    response = requests.get(url)
    info = response.json()
    if info['totalResults'] == 0:
        responses.say("Couldn't find any articles about that :(")
    for i in range(10 if info['totalResults'] >= 10 else info['totalResults']):
        top_article = info['articles'][i]
        responses.say(top_article['title'] + '\n' + top_article['url'])


def get_date():
    now = datetime.datetime.now()
    date = now - datetime.timedelta(days=7)
    return str(date).split()[0]
