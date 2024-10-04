from flask import Blueprint, render_template, session, redirect, url_for

from search_information import news_search, events_search, get_top_bar_information

main_page_blueprint = Blueprint('main_page', __name__)

@main_page_blueprint.route('/')
def main_page():
    if 'user_id' in session:
        all_news = news_search()
        all_events = events_search()

        user_information = get_top_bar_information(session['user_id'])

        return render_template(
            'index.html',
            all_news=all_news,
            all_events=all_events,
            is_admin=session['is_admin'],
            user_information=user_information
        )

    return redirect(url_for('authorization_page.authorization_page'))