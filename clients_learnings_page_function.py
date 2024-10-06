from flask import Blueprint, render_template

from search_information import news_search

clients_learnings_page_blueprint = Blueprint('clients_learnings_page', __name__)

@clients_learnings_page_blueprint.route('/clients-learnings')
def clients_learnings_page():
    all_news = news_search()

    return render_template(
        'clients-learnings.html',
        all_news=all_news
    )