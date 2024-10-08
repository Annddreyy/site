from flask import Blueprint, render_template, session, url_for
from werkzeug.utils import redirect

from search_information import news_search, get_top_bar_information, get_departments, clients_search

clients_weekends_page_blueprint = Blueprint('clients_weekends_page', __name__)

@clients_weekends_page_blueprint.route('/clients-weekends')
def clients_weekends_page():
    if 'user_id' in session:
        all_news = news_search()

        user_information = get_top_bar_information(session['user_id'])

        departments = get_departments()
        clients = clients_search()

        return render_template(
            'clients-weekends.html',
            all_news=all_news,
            user_information=user_information,
            is_admin=session['is_admin'],
            departments=departments,
            clients=clients
        )

    return redirect(url_for('authorization_page.authorization_page'))