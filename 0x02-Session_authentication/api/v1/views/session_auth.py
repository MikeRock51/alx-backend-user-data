#!/usr/bin/env python3
"""Session authentication module"""

from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from api.v1.views.users import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def sessionAuthenticate():
    """"Handles all routes for the session authentication"""
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    user: User = User().search({"email": email})

    if not user:
        abort(404)

    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    sessionID = auth.create_session(user.id)

    response = jsonify(user.to_json())
    response.set_cookie(getenv("SESSION_NAME"), sessionID)
    return make_response(response, 201)
