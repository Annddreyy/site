import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

BASE_URL = "http://127.0.0.1:2345/api/v1"


@app.route('/')
def main_page():
    all_news = news_search()
    all_events = events_search()

    return render_template(
        'index.html',
        all_news=all_news,
        all_events=all_events
    )


@app.route('/news/<int:news_id>')
def news_page(news_id):
    response = requests.get(f'{BASE_URL}/news/{news_id}').json()[0]

    all_news = news_search()

    news = [
        response['id'],
        response['title'],
        response['description'],
        response['image_path']
    ]

    return render_template(
        'news-page.html',
        news=news,
        all_news=all_news
    )


@app.route('/events/<int:event_id>')
def event_page(event_id):
    response = requests.get(f'{BASE_URL}/events/{event_id}').json()[0]

    all_news = news_search()

    event = [
        response['id'],
        response['title'],
        response['description'],
        response['image_path']
    ]

    return render_template(
        'event-page.html',
        event=event,
        all_news=all_news
    )

@app.route('/new_news', methods=['GET', 'POST'])
def new_news_page():
    if request.method == 'POST':
        title = request.form.get('news-title')
        description = request.form.get('news-text')
        date = request.form.get('news-date')
        image_path = ''

        file = request.files['image']

        if file.filename == '':
            return 'Файл не выбран'

        if file.filename.endswith('.jpg') or file.filename.endswith('.png'):
            image_path = file.filename
            file.save('static/company_files/news_images/' + image_path)


        news = {
            'title': title,
            'description': description,
            'date': date,
            'author': 4, #TODO
            'image_path': 'news_images/' + image_path
        }

        requests.post(url=f'{BASE_URL}/news', json=news)

        return redirect(url_for('new_news_page'))

    all_news = news_search()

    return render_template(
        'new-news.html',
        all_news=all_news
    )


@app.route('/new_event', methods=['GET', 'POST'])
def new_event_page():
    if request.method == 'POST':
        title = request.form.get('event-title')
        text = request.form.get('event-text')
        date_start = request.form.get('event-date-start')
        date_end = request.form.get('event-date-end')
        event_type = request.form.get('event-type')
        image_path = ''

        file = request.files['image']

        if file.filename == '':
            return 'Файл не выбран'

        if file.filename.endswith('.jpg') or file.filename.endswith('.png'):
            image_path = file.filename
            file.save('static/company_files/events/' + image_path)

        event = {
            'title': title,
            'text': text,
            'date_start': date_start,
            'date_end': date_end,
            'event_type': event_type,
            'author': 4, #TODO
            'image_path': 'events/' + image_path
        }

        requests.post(url=f'{BASE_URL}/events', json=event)
        return redirect(url_for('new_event_page'))

    all_news = news_search()
    response = requests.get(f'{BASE_URL}/event_types').json()

    event_types = []
    for event_type in response:
        event_types.append(
            [
                event_type['id'],
                event_type['title']
            ]
        )

    return render_template(
        'new-event.html',
        all_news=all_news,
        event_types=event_types
    )


@app.route('/new_learning')
def new_learning_page():
    all_news = news_search()

    return render_template(
        'new-learning.html',
        all_news=all_news
    )


@app.route('/personal')
def personal_page():
    all_news = news_search()

    return render_template(
        'personal.html',
        all_news=all_news
    )


@app.route('/resume')
def resume_page():
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

    all_news = news_search()

    return render_template(
        'resume.html',
        all_resumes=all_resumes,
        all_news=all_news
    )


@app.route('/clients-events')
def clients_events_page():
    all_news = news_search()

    return render_template(
        'clients-events.html',
        all_news=all_news
    )


@app.route('/clients-learnings')
def clients_learnings_page():
    all_news = news_search()

    return render_template(
        'clients-learnings.html',
        all_news=all_news
    )


@app.route('/clients-weekends')
def clients_weekends_page():
    all_news = news_search()

    return render_template(
        'clients-weekends.html',
        all_news=all_news
    )


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


if __name__ == '__main__':
    app.run(debug=True)