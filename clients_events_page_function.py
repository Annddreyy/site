from flask import Blueprint, render_template, session, redirect, url_for, request

from search_information import news_search, get_top_bar_information, get_departments, clients_search, events_search

clients_events_page_blueprint = Blueprint('clients_events_page', __name__)

@clients_events_page_blueprint.route('/clients-events')
def clients_events_page():
    if 'user_id' in session:
        all_news = news_search()

        user_information = get_top_bar_information(session['user_id'])

        departments = get_departments()
        clients = clients_search()

        all_events = events_search()

        client_id = request.args.get('client')
        if client_id:
            client_id = int(client_id)
            events = []
            for event in all_events:
                if client_id in event[9]:
                    events.append(event)

            return render_template(
                'clients-events.html',
                all_news=all_news,
                user_information=user_information,
                is_admin=session['is_admin'],
                departments=departments,
                clients=clients,
                all_events=events
            )

        return render_template(
            'clients-events.html',
            all_news=all_news,
            user_information=user_information,
            is_admin=session['is_admin'],
            departments=departments,
            clients=clients,
            all_events=all_events
        )

    return redirect(url_for('authorization_page.authorization_page'))