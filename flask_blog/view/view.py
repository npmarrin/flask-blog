"""
    View Helper Functions
"""

# https://docs.python.org/3/library/functools.html#functools.wraps
from functools import wraps
from flask import flash, redirect, session, url_for

LOGIN_ERROR = 'You need to login first.'
REDIRECT_LOGIN_ERROR = 'users.login'


def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            flash(LOGIN_ERROR)
            return redirect(url_for(REDIRECT_LOGIN_ERROR))
    return wrap
