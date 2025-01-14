from flask import render_template, g
from app.main import bp
from app.extensions.identity import Identity

@bp.route('/')
def index():
    org_data = {
        'org1': {
            'total_users': 1256,
            'pending_tasks': 42,
            'completed_projects': 89,
            'performance': 75,
            'sales': {
                'north': 70,
                'south': 50,
                'east': 60,
                'west': 80
            }
        },
        'org2': {
            'total_users': 980,
            'pending_tasks': 12,
            'completed_projects': 150,
            'sales': {
                'north': 55,
                'south': 65,
                'east': 45,
                'west': 95
            }
        }
    }

    g.user = Identity.get_user_info()
    org = 'no_org'
    if g.user:
        if len(g.user["organization"]) > 0:
            org = g.user["organization"][0]

    data = org_data.get(org, {})


    return render_template('index.html', g=g, data=data)
