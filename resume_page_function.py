import requests
from flask import render_template, Blueprint, request, session, url_for, abort
from werkzeug.utils import redirect

from env_variables import BASE_URL
from search_information import news_search, get_jobs, get_resumes

resume_page_blueprint = Blueprint('resume_page', __name__)

@resume_page_blueprint.route('/resume', methods=['GET', 'POST'])
def resume_page():
    if 'user_id' in session:
        if session['is_admin']:
            all_resumes = get_resumes()
            all_news = news_search()
            all_jobs = get_jobs()

            if request.method == 'POST':
                job_id = request.form.get('job-title')
                response = requests.get(f'{BASE_URL}/jobs/{job_id}').json()['title']
                new_resumes = []
                for resume in all_resumes:
                    if resume[2] == response:
                        new_resumes.append(resume)

                session['resume'] = new_resumes

                return redirect(url_for('resume_page.resume_page'))

            if 'resume' in session:
                all_resumes = session['resume']

            return render_template(
                'resume.html',
                all_resumes=all_resumes,
                all_news=all_news,
                all_jobs = all_jobs
            )
        else:
            return abort(404)
    else:
        return redirect(url_for('authorization_page.authorization_page'))

@resume_page_blueprint.route('/reset_resume_filter', methods=['GET'])
def reset_resume_filter():
    if 'resume' in session:
        session.pop('resume')
    return redirect(url_for('resume_page.resume_page'))
