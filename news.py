import requests

API_KEY = 'c10aaad5b172490b9ff1b954d6cec496'


def get_top_news():
    top_url = 'http://newsapi.org/v2/top-headlines?country=au&apiKey=' + API_KEY
    return get_news(top_url)


def get_news_about(topic):
    question_url = 'http://newsapi.org/v2/everything?q=' + topic + '&apiKey=' + API_KEY
    return get_news(question_url)


def get_news(url):
    response = requests.get(url)
    info = response.json()
    message = ""
    for i in range(3):
        top_article = info['articles'][i]
        message += top_article['title'] + '\n' + top_article['url'] + '\n'
    return message
