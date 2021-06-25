from flask import Blueprint, request
from flask_login import login_required

passmanager = Blueprint('passmanager', __name__)


@passmanager.route('/password', methods=['POST'])
@login_required
def password():
    site = request.form['site']
    #print("Password register for", site)
