from flask import render_template, g
from app.main import bp
from app.extensions.identity import Identity

@bp.route('/')
def index():
    g.user = Identity.get_user_info()
    print(g.user)
    return render_template('index.html', g=g)
