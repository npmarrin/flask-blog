import datetime

from flask import Blueprint, request, current_app, url_for, redirect, session
from flask_blog.view.decorators import validate_form_on_submit
from flask_wtf import FlaskForm

from .models import User
from .forms import RegistrationForm, LoginForm


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
@validate_form_on_submit(LoginForm, 'auth/login.html')
def login():
    """
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            {}
    return render_template('auth/login.html', form=form)
    """
    form = LoginForm()
    user = User.authenticate(form.email.data, form.password.data)
    if user is not None:
        user.set_user_session()
        response = redirect(url_for('hello_world'))
        if request.form.get('remember'):
            token = user.remember_me_token(
                current_app.config['SECRET_KEY'],
                datetime.timedelta(
                    days=current_app.config['REMEMBER_ME_DAYS']
                ),
                current_app.config['SERVER_NAME'],
                current_app.config['JWT_ALGORITHM']
            )
            response.set_cookie(
                'remember_me',
                token,
                secure=current_app.config['OTHER_COOKIE_SECURE']
            )

        return response
    return redirect(url_for('auth.register'))


@auth.route('/register', methods=['GET', 'POST'])
@validate_form_on_submit(RegistrationForm, 'auth/register.html')
def register():
    """
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            {}
    return render_template('auth/register.html', form=form)
    """
    form = RegistrationForm()
    User.register(form.name.data, form.email.data, form.password.data)
    response = redirect(url_for('hello_world'))
    response.set_cookie('remember_me', '', expires=0)
    return response


@auth.route('/logout', methods=['POST'])
def logout():
    # Basic form to validate CSRF
    form = FlaskForm()
    if form.validate_on_submit():
        response = redirect(url_for('auth.register'))
        response.set_cookie('remember_me', '', expires=0)
        session.pop('user', None)
        return response
