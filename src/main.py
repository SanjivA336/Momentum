from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('main/static/index.html')

@main.route('/profile')
#@login_required
def profile():
    return render_template('main/profile.html')