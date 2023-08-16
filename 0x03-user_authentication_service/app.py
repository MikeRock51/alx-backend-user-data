#!/usr/bin/env python3
"""Flask Application"""

from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from auth import Auth

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
AUTH = Auth()


@app.route('/', strict_slashes=False)
def home() -> str:
    """Home route"""
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def createUser() -> str:
    """Creates a new user"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"}), 201


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def getSession() -> str:
    """Creates a session for the user"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(400)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie('session_id', session_id)

    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
