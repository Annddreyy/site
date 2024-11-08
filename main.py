from flask import Flask, render_template, session, redirect, url_for

from authorization_page_function import authorization_page_blueprint
from clients_events_page_function import clients_events_page_blueprint
from clients_learnings_page_function import clients_learnings_page_blueprint
from clients_weekends_page_function import clients_weekends_page_blueprint
from env_variables import SECRET_KEY
from event_page_function import event_page_blueprint
from main_page_function import main_page_blueprint
from new_event_page_function import new_event_page_blueprint
from new_learning_page import new_learning_page_blueprint
from new_news_page_function import new_news_page_blueprint
from news_page_function import news_page_blueprint
from out_page_function import out_page_blueprint
from personal_page_function import personal_page_blueprint
from resume_page_function import resume_page_blueprint
from user_profile_page_function import user_profile_page_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

app.register_blueprint(main_page_blueprint)
app.register_blueprint(out_page_blueprint)
app.register_blueprint(authorization_page_blueprint)
app.register_blueprint(news_page_blueprint)
app.register_blueprint(event_page_blueprint)
app.register_blueprint(new_news_page_blueprint)
app.register_blueprint(new_event_page_blueprint)
app.register_blueprint(new_learning_page_blueprint)
app.register_blueprint(user_profile_page_blueprint)
app.register_blueprint(personal_page_blueprint)
app.register_blueprint(resume_page_blueprint)
app.register_blueprint(clients_events_page_blueprint)
app.register_blueprint(clients_learnings_page_blueprint)
app.register_blueprint(clients_weekends_page_blueprint)

@app.errorhandler(404)
def error_404_page(error):
    if 'user_id' in session:
        return render_template('error-page.html')
    return redirect(url_for('authorization_page.authorization_page'))

@app.errorhandler(500)
def error_500_page(error):
    if 'user_id' in session:
        return render_template('error-page.html')
    return redirect(url_for('authorization_page.authorization_page'))

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")