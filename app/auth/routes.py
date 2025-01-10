from app.extensions.identity import Identity
from config import REDIRECT_URI
from app.auth import bp
from urllib.parse import urlparse

CALLBACK_URL = urlparse(REDIRECT_URI).path.replace("/auth", "", 1)

from flask import (
    flash, redirect,request, session, url_for, jsonify
)

@bp.route('/login')
def login():
    return redirect(Identity.get_authorization_url())

@bp.route('/logout')
def logout():
    return redirect(Identity.logout() or url_for("main.index"))

@bp.route(CALLBACK_URL)
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    if code is not None:
        #! Remove next line in production
        session["state"] = state
        #!
        if state is not None and not state == session.get("state"):
            flash("Invalid state parameter", "error")
            return redirect(url_for("main.index"))
        try:
            session["access_token"] = Identity.get_access_token(code, state)
            return redirect(url_for("main.index"))
        except RuntimeError as e:
            flash(str(e), "error")
            return redirect(url_for("main.index"))
    else:
        flash("Error during login", "error")
        return redirect(url_for("main.index"))

@bp.route('/me')
@Identity.middleguard
def me(user_info=None):
    if user_info:
        return jsonify(user_info.to_dict())
    else:
        return jsonify({"error": "No user info available"}), 500