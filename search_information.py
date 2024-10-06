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

def get_departments():
    response = requests.get(f'{BASE_URL}/departments').json()

    departments = []
    for department in response:
        departments.append(
            [
                department['id'],
                department['title']
            ]
        )

    return departments

def get_top_bar_information(client_id):
    client = requests.get(f'{BASE_URL}/clients/{client_id}').json()[0]

    return [client['photo'], f'{client['surname']} {client['name'][0]}. {client['patronymic'][0]}.']

def clients_search():
    response = requests.get(f'{BASE_URL}/clients').json()

    clients = []
    for client in response:
        clients.append(
            [
                client['id'],
                client['FIO'],
                client['photo'],
                client['adress'],
                client['phone'],
                client['email'],
                client['birthday_date'],
                client['cabinet'],
                client['dop_information'],
                client['department'],
                client['job'],
                client['role']
            ]
        )

    return clients

def get_jobs():
    response = requests.get(f'{BASE_URL}/jobs').json()

    jobs = []
    for job in response:
        jobs.append(
            [
                job['id'],
                job['title']
            ]
        )

    return jobs

def get_resumes():
    response = requests.get(f'{BASE_URL}/resume').json()

    all_resumes = []
    for resume in response:
        all_resumes.append(
            [
                resume['id'],
                resume['author'],
                resume['job_title'],
                resume['file_path']
            ]
        )

    return all_resumes