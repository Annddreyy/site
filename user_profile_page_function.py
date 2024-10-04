import requests
from flask import Blueprint, render_template, session, request, redirect, url_for

from env_variables import BASE_URL
from search_information import news_search, get_top_bar_information

user_profile_page_blueprint = Blueprint('user_profile_page', __name__)

@user_profile_page_blueprint.route('/user-profile', methods=['GET', 'POST'])
def user_profile_page():
    if 'user_id' in session:
        if request.method == 'POST':
            surname = request.form.get('surname')
            name = request.form.get('name')
            patronymic = request.form.get('patronymic')
            adress = request.form.get('adress')
            phone = request.form.get('phone')
            email = request.form.get('email')
            image_path = ''

            file = request.files['user-image-file']

            if file:
                image_path = file.filename
                file.save('static/company_files/photo/' + image_path)

            user_edit_information = {}

            if surname:
                user_edit_information['surname'] = surname
            if name:
                user_edit_information['name'] = name
            if patronymic:
                user_edit_information['patronymic'] = patronymic
            if adress:
                user_edit_information['adress'] = adress
            if phone:
                user_edit_information['phone'] = phone
            if email:
                user_edit_information['email'] = email
            if image_path:
                user_edit_information['image_path'] = 'photo/' + image_path

            requests.patch(url=f'{BASE_URL}/clients/{session['user_id']}', json=user_edit_information)

            return redirect(url_for('user_profile_page.user_profile_page'))

        all_news = news_search()

        user_information = get_top_bar_information(session['user_id'])

        response = requests.get(f'{BASE_URL}/clients/{session['user_id']}').json()[0]

        user = [
            response['surname'],
            response['name'],
            response['patronymic'],
            response['adress'],
            response['phone'],
            response['email'],
            response['photo']
        ]

        return render_template(
            'user-profile.html',
            all_news=all_news,
            user_information=user_information,
            is_admin=session['is_admin'],
            user=user
        )

    return redirect(url_for('authorization_page.authorization_page'))