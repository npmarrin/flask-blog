from flask import Blueprint, jsonify
from flask_blog.auth.decorators import requires_basic_auth

api = Blueprint('api', __name__)


@api.route('/hello-world', methods=['GET'])
@requires_basic_auth
def login():
    return jsonify({'message': 'Hello World!'})
