import requests
from flask import request

from env_variables import BASE_URL

def news_search():
    response = requests.get(f'{BASE_URL}/news').json()

    find_word = request.args.get('news-search')
    sort_type = request.args.get('sort-type')

    if not find_word:
        find_word = ""
    find_word = find_word.lower()

    if not sort_type:
        sort_type = ""


    all_news = []
    for news in response:
        if find_word in news['title'].lower() or find_word in news['description'].lower():
            all_news.append(
                [
                    news['id'],
                    news['title'],
                    news['description'][:250] + '...',
                    news['date'],
                    news['author'],
                    news['image_path'],
                    news['photo']
                ]
            )

    if sort_type:
        indexes = {
            'title': 1,
            'date': 3,
            'author': 4
        }
        all_news.sort(key=lambda x: x[indexes[sort_type]])

    return all_news


def events_search():
    response = requests.get(f'{BASE_URL}/events').json()

    events = []
    for event in response:
        events.append(
            [
                event['id'],
                event['title'],
                event['description'],
                event['event_type'],
                event['author'],
                event['photo'],
                event['image_path'],
                event['date_start'],
                event['date_end']
            ]
        )

    return events