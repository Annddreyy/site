import requests
from flask import render_template, Blueprint

from env_variables import BASE_URL
from search_information import news_search

news_page_blueprint = Blueprint('news_page', __name__)

@news_page_blueprint.route('/news/<int:news_id>')
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