"""
    View Decorator Functions
"""

# https://docs.python.org/3/library/functools.html#functools.wraps
from functools import wraps

from flask import request, jsonify, render_template


def validate_form_on_submit(form_name, template):
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            form = form_name()
            if request.method == 'POST':
                if form.validate_on_submit():
                    return func(*args, **kwargs)
            return render_template(template, form=form)
        return wrap
    return decorator
