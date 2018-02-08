from flask_blog.application import create_app
from flask_blog.extensions import db
from flask_migrate import Migrate
from flask_blog.models import User
from datetime import datetime

app = create_app()
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


@app.route('/')
def hello():
    return 'Hello World! ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
