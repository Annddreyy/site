import requests
from flask import render_template, Blueprint, request, redirect, url_for, flash, session, abort

from env_variables import BASE_URL
from search_information import news_search, get_top_bar_information

new_learning_page_blueprint = Blueprint('new_learning_page', __name__)

@new_learning_page_blueprint.route('/new_learning', methods=['GET', 'POST'])
def new_learning_page():
    if 'user_id' in session:
        if session['is_admin']:
            if request.method == 'POST':
                try:
                    title = request.form.get('learning-title')
                    text = request.form.get('learning-text')
                    date_start = request.form.get('learning-date-start')
                    date_end = request.form.get('learning-date-end')

                    file = request.files['image']

                    image_path = file.filename
                    file.save('static/company_files/learnings/' + image_path)

                    learning = {
                        'title': title,
                        'text': text,
                        'date_start': date_start,
                        'date_end': date_end,
                        'author': session['user_id'],
                        'image_path': 'learnings/' + image_path
                    }

                    requests.post(url=f'{BASE_URL}/learnings', json=learning)

                    return redirect(url_for('new_learning_page.new_learning_page')), flash('Обучение успешно добавлено!')
                except:
                    return redirect(url_for('new_learning_page.new_learning_page')), flash('При добавлении обучения произошла ошибка!')

            all_news = news_search()

            user_information = get_top_bar_information(session['user_id'])

            return render_template(
                'new-learning.html',
                all_news=all_news,
                is_admin=session['is_admin'],
                user_information=user_information
            )

        return abort(404)

    return redirect(url_for('authorization_page.authorization_page'))