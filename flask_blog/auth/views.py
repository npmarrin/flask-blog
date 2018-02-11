from flask import render_template, redirect, url_for
from flask import Blueprint, request, jsonify
from flask_blog import db, bcrypt

from .models import User


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        user = User.query.filter_by(email=request.form['email']).first()

        if not user:
            return redirect(url_for('.register'))

        if user.verify_password(request.form['password']):
            return jsonify({'name': user.name, 'email': user.email})
        else:
            return jsonify({'error': 'Username or Password invalid'})
    else:
        return render_template('auth/login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        json_response = {'register_name': '', 'register_email': '', 'register_password': ''}

        if 'name' in request.form.keys():
            json_response['register_name'] = request.form['name']

        if 'email' in request.form.keys():
            json_response['register_email'] = request.form['email']

        if 'password' in request.form.keys():
            json_response['register_password'] = request.form['password']

        registrant = User(name=json_response['register_name'],
                          email=json_response['register_email'])
        registrant.password = json_response['register_password']

        db.session.add(registrant)
        db.session.commit()
        return jsonify(json_response)
    else:
        return render_template('auth/register.html')
