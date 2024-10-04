import requests
from flask import Flask, render_template

from authorization_page_function import authorization_page_blueprint
from env_variables import SECRET_KEY
from event_page_function import event_page_blueprint
from main_page_function import main_page_blueprint
from new_event_page_function import new_event_page_blueprint
from new_learning_page import new_learning_page_blueprint
from new_news_page_function import new_news_page_blueprint
from news_page_function import news_page_blueprint
from out_page_function import out_page_blueprint
from user_profile_page_function import user_profile_page_blueprint
from search_information import news_search

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

BASE_URL = "http://127.0.0.1:2345/api/v1"

app.register_blueprint(main_page_blueprint)
app.register_blueprint(out_page_blueprint)
app.register_blueprint(authorization_page_blueprint)
app.register_blueprint(news_page_blueprint)
app.register_blueprint(event_page_blueprint)
app.register_blueprint(new_news_page_blueprint)
app.register_blueprint(new_event_page_blueprint)
app.register_blueprint(new_learning_page_blueprint)
app.register_blueprint(user_profile_page_blueprint)


@app.route('/resume')
def resume_page():
    response = requests.get(f'{BASE_URL}/resume').json()

    all_resumes = []
    for resume in response:
        all_resumes.append(
            [
                resume['id'],
                resume['author'],
                resume['job_title'],
                resume['file_path']
            ]
        )

    all_news = news_search()

    return render_template(
        'resume.html',
        all_resumes=all_resumes,
        all_news=all_news
    )


@app.route('/clients-events')
def clients_events_page():
    all_news = news_search()

    return render_template(
        'clients-events.html',
        all_news=all_news
    )


@app.route('/clients-learnings')
def clients_learnings_page():
    all_news = news_search()

    return render_template(
        'clients-learnings.html',
        all_news=all_news
    )


@app.route('/clients-weekends')
def clients_weekends_page():
    all_news = news_search()

    return render_template(
        'clients-weekends.html',
        all_news=all_news
    )

if __name__ == '__main__':
    app.run(debug=True)