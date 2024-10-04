import requests
from flask import render_template, Blueprint

from env_variables import BASE_URL
from search_information import news_search

event_page_blueprint = Blueprint('event_page', __name__)

@event_page_blueprint.route('/events/<int:event_id>')
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