import requests
from flask import render_template, Blueprint, session, redirect, url_for

from env_variables import BASE_URL
from search_information import news_search, get_top_bar_information

news_page_blueprint = Blueprint('news_page', __name__)

@news_page_blueprint.route('/news/<int:news_id>')
def news_page(news_id):
    if 'user_id' in session:
        response = requests.get(f'{BASE_URL}/news/{news_id}').json()[0]

        all_news = news_search()

        news = [
            response['id'],
            response['title'],
            response['description'],
            response['image_path']
        ]

        user_information = get_top_bar_information(session['user_id'])

        return render_template(
            'news-page.html',
            news=news,
            all_news=all_news,
            is_admin=session['is_admin'],
            user_information=user_information
        )

    return redirect(url_for('authorization_page.authorization_page'))