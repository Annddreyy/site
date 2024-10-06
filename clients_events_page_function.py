from flask import Blueprint, render_template

from search_information import news_search

clients_events_page_blueprint = Blueprint('clients_events_page', __name__)

@clients_events_page_blueprint.route('/clients-events')
def clients_events_page():
    all_news = news_search()

    return render_template(
        'clients-events.html',
        all_news=all_news
    )