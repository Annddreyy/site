import requests
from flask import render_template, Blueprint, request, redirect, url_for, flash

from env_variables import BASE_URL
from search_information import news_search

new_news_page_blueprint = Blueprint('new_news_page', __name__)

@new_news_page_blueprint.route('/new_news', methods=['GET', 'POST'])
def new_news_page():
    if request.method == 'POST':
        try:
            title = request.form.get('news-title')
            description = request.form.get('news-text')
            date = request.form.get('news-date')

            file = request.files['image']

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

            return redirect(url_for('new_news_page.new_news_page')), flash('Новость успешно добавлена!')
        except:
            return redirect(url_for('new_news_page.new_news_page')), flash('При добавлении новости произошла ошибка!!')

    all_news = news_search()

    return render_template(
        'new-news.html',
        all_news=all_news
    )