import requests
from flask import render_template, Blueprint, session, url_for
from werkzeug.utils import redirect

from env_variables import BASE_URL
from search_information import news_search, get_top_bar_information

event_page_blueprint = Blueprint('event_page', __name__)

@event_page_blueprint.route('/events/<int:event_id>')
def event_page(event_id):
    if 'user_id' in session:
        response = requests.get(f'{BASE_URL}/events/{event_id}').json()

        all_news = news_search()

        event = [
            response['id'],
            response['title'],
            response['description'],
            response['image_path']
        ]

        user_information = get_top_bar_information(session['user_id'])

        return render_template(
            'event-page.html',
            event=event,
            all_news=all_news,
            is_admin=session['is_admin'],
            user_information=user_information
        )
    else:
        return redirect(url_for('authorization_page.authorization_page'))