from functools import wraps
from flask import request, Response, session, redirect, url_for

from .models import User


def basic_auth_challenge():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Missing or incorrect authentication credentials',
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_basic_auth(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        auth = request.authorization
        if not auth or not User.authenticate(auth.username, auth.password):
            return basic_auth_challenge()
        return func(*args, **kwargs)
    return wrap


def login_required(secret, issuer):
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            if 'user' in session or\
                ('remember_me' in request.cookies and
                 User.validate_remember_me_token(
                     request.cookies['remember_me'],
                     secret,
                     issuer
                 )):
                return func(*args, **kwargs)

            return redirect(url_for('auth.register'))
        return wrap
    return decorator
