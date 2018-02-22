from flask_migrate import Migrate
from flask import render_template, session, request, jsonify, url_for

from flask_blog.application import create_app
from flask_blog.extensions import db
from flask_blog.auth.models import User
from flask_blog.auth.decorators import login_required


app = create_app()
migrate = Migrate(app, db)


@app.route('/')
@login_required(app.config['SECRET_KEY'], app.config['SERVER_NAME'])
def hello_world():
    return render_template('nav.html', user=session['user'])


@app.errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


@app.cli.command()
def list_routes():
    """List all app routes"""
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote(
            "{:35s} {:35s} {}".format(
                rule.endpoint,
                methods,
                url
            )
        )
        output.append(line)

    for line in sorted(output):
        print(line)
