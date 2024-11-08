import requests
from flask import render_template, Blueprint, request, redirect, url_for, flash, session, abort

from env_variables import BASE_URL
from search_information import news_search, get_top_bar_information

new_news_page_blueprint = Blueprint('new_news_page', __name__)

@new_news_page_blueprint.route('/new_news', methods=['GET', 'POST'])
def new_news_page():
    if 'user_id' in session:
        if session['is_admin']:
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
                        'author': session['user_id'],
                        'image_path': 'news_images/' + image_path
                    }

                    requests.post(url=f'{BASE_URL}/news', json=news)

                    return redirect(url_for('new_news_page.new_news_page')), flash('Новость успешно добавлена!')
                except:
                    return redirect(url_for('new_news_page.new_news_page')), flash('При добавлении новости произошла ошибка!!')

            all_news = news_search()

            user_information = get_top_bar_information(session['user_id'])

            return render_template(
                'new-news.html',
                all_news=all_news,
                is_admin=session['is_admin'],
                user_information=user_information
            )
        return abort(404)

    return redirect(url_for('authorization_page.authorization_page'))