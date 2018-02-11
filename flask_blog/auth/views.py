from flask import render_template, redirect, url_for
from flask import Blueprint, request, jsonify
from flask_blog import db

from .models import User
from .forms import RegistrationForm, LoginForm


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=request.form['email']).first()

            if user and user.verify_password(request.form['password']):
                return jsonify({'name': user.name, 'email': user.email})
        return jsonify(form.errors)
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            registrant = User(name=request.form['name'],
                              email=request.form['email'])

            registrant.password = request.form['password']

            db.session.add(registrant)
            db.session.commit()
            return jsonify({'name': registrant.name, 'email': registrant.email})
        return jsonify(form.errors)
    return render_template('auth/register.html', form=form)
