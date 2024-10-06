import requests
from flask import render_template, Blueprint

from env_variables import BASE_URL
from search_information import news_search, get_jobs, get_resumes

resume_page_blueprint = Blueprint('resume_page', __name__)

@resume_page_blueprint.route('/resume')
def resume_page():
    all_resumes = get_resumes()
    all_news = news_search()
    all_jobs = get_jobs()

    print(all_jobs)

    return render_template(
        'resume.html',
        all_resumes=all_resumes,
        all_news=all_news,
        all_jobs = all_jobs
    )
