from app.extensions.identity import Identity
from config import REDIRECT_URI
from app.auth import bp
from urllib.parse import urlparse

CALLBACK_URL = urlparse(REDIRECT_URI).path

from flask import (
    flash, redirect,request, session, url_for, jsonify
)

@bp.route('/login')
def login():
    return redirect(Identity.get_authorization_url())

@bp.route('/logout')
def logout():
    Identity.logout()
    return redirect(url_for('index'))

@bp.route(CALLBACK_URL)
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    if code is not None:
        if state is not None and not state == session.get("state"):
            flash("Invalid state parameter", "error")
            return redirect(url_for("index"))
        Identity.get_access_token(code)
        return redirect(url_for("index"))
    else:
        flash("Error during login", "error")
        return redirect(url_for("index"))

@Identity.middleguard
@bp.route('/me')
def me():
    user_info = Identity.get_user_info()
    if user_info:
        return jsonify(user_info)
    else:
        return redirect(url_for("auth.login"))