#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """Test register route of the web server"""
    form = {"email": email, "password": password}
    response = requests.post('http://127.0.0.1:5000/users', data=form)
    expResponse = {"email": email, "message": "user created"}

    assert response.json() == expResponse


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests the log in route of the web server with wrong password"""
    form = {"email": email, "password": password}
    response = requests.post('http://127.0.0.1:5000/sessions', data=form)

    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Tests the log in route of the web server"""
    form = {"email": email, "password": password}
    response = requests.post('http://127.0.0.1:5000/sessions', data=form)
    expResponse = {"email": email, "message": "logged in"}

    assert response.json() == expResponse
    assert "session_id" in response.cookies
    return response.cookies['session_id']


def profile_unlogged() -> None:
    """Tests the profile route of the web server without logging in"""
    response = requests.get('http://127.0.0.1:5000/profile')

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Tests the profile route of the web server"""
    cookies = {'session_id': session_id}
    response = requests.get('http://127.0.0.1:5000/profile', cookies=cookies)
    expResponse = {"email": response.json()['email']}

    assert response.json() == expResponse


def log_out(session_id: str) -> None:
    """Tests the log out functionality of the web server"""
    cookies = {'session_id': session_id}
    response = requests.delete(
        'http://127.0.0.1:5000/sessions', cookies=cookies)

    assert response.status_code != 403


def reset_password_token(email: str) -> str:
    """Tests the reset password token functionality of the web server"""
    form = {"email": email}
    response = requests.post('http://127.0.0.1:5000/reset_password', data=form)
    expResponse = {"email": email,
                   "reset_token": response.json()['reset_token']}

    assert response.json() == expResponse
    return response.json()['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests the update password functionality of the web server"""
    form = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put('http://127.0.0.1:5000/reset_password', data=form)
    expResponse = {"email": email, "message": "Password updated"}

    assert response.json() == expResponse


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
