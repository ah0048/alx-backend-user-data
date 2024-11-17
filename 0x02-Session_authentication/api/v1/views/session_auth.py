#!/usr/bin/env python3
""" Module of session views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def session_login():
    '''session login'''
    email = request.form.get("email", default=None)
    if email == "" or email is None:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password", default=None)
    if password == "" or password is None:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        user = users[0]
        session_id = auth.create_session(user.id)
        session_name = os.getenv('SESSION_NAME')
        response = jsonify(user.to_json())
        response.set_cookie(session_name, session_id)
        return response
    else:
        return jsonify({"error": "wrong password"}), 401


@app_views.route("/auth_session/logout", methods=["DELETE"],
                 strict_slashes=False)
def session_delete():
    '''delete session when logout'''
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(404)
