import requests
from flask import render_template, Blueprint, request, redirect, url_for, flash, session, abort

from env_variables import BASE_URL
from search_information import news_search

new_event_page_blueprint = Blueprint('new_event_page', __name__)

@new_event_page_blueprint.route('/new_event', methods=['GET', 'POST'])
def new_event_page():
    if 'user_id' in session:
        if session['is_admin']:
            if request.method == 'POST':
                try:
                    title = request.form.get('event-title')
                    text = request.form.get('event-text')
                    date_start = request.form.get('event-date-start')
                    date_end = request.form.get('event-date-end')
                    event_type = request.form.get('event-type')

                    file = request.files['image']

                    image_path = file.filename
                    file.save('static/company_files/events/' + image_path)

                    event = {
                        'title': title,
                        'text': text,
                        'date_start': date_start,
                        'date_end': date_end,
                        'event_type': event_type,
                        'author': session['user_id'],
                        'image_path': 'events/' + image_path
                    }

                    requests.post(url=f'{BASE_URL}/events', json=event)

                    return redirect(url_for('new_event_page.new_event_page')), flash('Событие успешно добавлено!')
                except:
                    return redirect(url_for('new_event_page.new_event_page')), flash('При добавлении события произошла ошибка!!')

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
        return abort(404)

    return redirect(url_for('authorization_page.authorization_page'))