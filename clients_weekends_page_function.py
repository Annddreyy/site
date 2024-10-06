from flask import Blueprint, render_template

from search_information import news_search

clients_weekends_page_blueprint = Blueprint('clients_weekends_page', __name__)

@clients_weekends_page_blueprint.route('/clients-weekends')
def clients_weekends_page():
    all_news = news_search()

    return render_template(
        'clients-weekends.html',
        all_news=all_news
    )