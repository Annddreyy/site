from flask import Blueprint, session, redirect, url_for

out_page_blueprint = Blueprint('out_page', __name__)

@out_page_blueprint.route('/out')
def out_page():
    session.clear()
    return redirect(url_for('main_page.main_page'))