import hashlib

import requests
from flask import Blueprint, session, redirect, url_for, request, render_template, flash

from env_variables import BASE_URL

authorization_page_blueprint = Blueprint('authorization_page', __name__)

@authorization_page_blueprint.route('/authorization', methods=['GET', 'POST'])
def authorization_page():
    if 'user_id' not in session:
        if request.method == 'POST':
            login = request.form.get('login')
            password = request.form.get('password')
            result = hashlib.sha256(password.encode()).hexdigest()

            response = requests.get(f'{BASE_URL}/authorization').json()

            for user in response:
                if user['login'] == login and user['password'] == result:
                    session['user_id'] = user['id']

                    response = requests.get(f'{BASE_URL}/clients/{user['id']}').json()

                    session['is_admin'] = response['role'] == 2

                    return redirect(url_for('main_page.main_page'))

            return redirect(url_for('authorization_page.authorization_page')), flash('Неверный логин или пароль!')
        return render_template('authorization.html')
    return redirect(url_for('main_page.main_page'))