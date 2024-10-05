import requests
from flask import Blueprint, render_template, session, request, url_for
from werkzeug.utils import redirect

from env_variables import BASE_URL
from search_information import get_top_bar_information, get_departments, news_search, clients_search

personal_page_blueprint = Blueprint('personal_page', __name__)
@personal_page_blueprint.route('/personal', methods=['GET', 'POST'])
def personal_page():
    user_information = get_top_bar_information(session['user_id'])
    departments = get_departments()
    all_news = news_search()
    clients = clients_search()

    if request.method == 'POST':
        client_id = request.form.get('client')
        new_client_json = requests.get(f'{BASE_URL}/clients/{client_id}').json()[0]
        print(client_id)

        new_client = [
            new_client_json['id'],
            new_client_json['surname'],
            new_client_json['name'],
            new_client_json['patronymic'],
            new_client_json['photo'],
            new_client_json['adress'],
            new_client_json['phone'],
            new_client_json['email'],
            new_client_json['birthday_date'],
            new_client_json['cabinet'],
            new_client_json['dop_information']
        ]

        session['client_card'] = new_client

        return redirect(url_for('personal_page.personal_page'))

    client = 'Undefined'
    if session.get('client_card'):
        client = session.get('client_card')

    return render_template(
        'personal.html',
        user_information=user_information,
        departments=departments,
        all_news=all_news,
        clients=clients,
        client=client
    )