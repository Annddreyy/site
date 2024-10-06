from flask import Blueprint, render_template, session

from search_information import news_search, get_top_bar_information

clients_learnings_page_blueprint = Blueprint('clients_learnings_page', __name__)

@clients_learnings_page_blueprint.route('/clients-learnings')
def clients_learnings_page():
    all_news = news_search()

    user_information = get_top_bar_information(session['user_id'])

    return render_template(
        'clients-learnings.html',
        all_news=all_news,
        user_information=user_information,
        is_admin=session['is_admin']
    )