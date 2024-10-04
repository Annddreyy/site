import requests
from flask import Blueprint, render_template, session

from env_variables import BASE_URL
from search_information import news_search, get_top_bar_information

user_profile_page_blueprint = Blueprint('user_profile_page', __name__)

@user_profile_page_blueprint.route('/user-profile')
def personal_page():
    all_news = news_search()

    user_information = get_top_bar_information(session['user_id'])

    response = requests.get(f'{BASE_URL}/clients/{session['user_id']}').json()[0]

    user = [
        response['surname'],
        response['name'],
        response['patronymic'],
        response['adress'],
        response['phone'],
        response['email'],
        response['photo']
    ]

    return render_template(
        'user-profile.html',
        all_news=all_news,
        user_information=user_information,
        is_admin=session['is_admin'],
        user=user
    )