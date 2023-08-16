#!/usr/bin/env python3
"""Flask Application"""

from flask import Flask, jsonify, request, abort, redirect
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

    return jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def getSession() -> str:
    """Creates a session for the user"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie('session_id', session_id)

    return res


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """Destroys the user session_id"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect('/')


@app.route('/profile', strict_slashes=False)
def userProfile():
    """Returns the user profile based of session_id"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
        Generates and returns a password reset
        token for a user based on email
    """
    email = request.form.get('email')

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
