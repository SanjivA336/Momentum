from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import User
from . import db

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('main/index.html')

@main.route('/info')
@login_required
def info():
    feet = ""
    inches = ""
    if(current_user.height != None):
        feet = current_user.height // 12
        inches = current_user.height % 12
    return render_template('profile/info.html', name=current_user.name, birthday=current_user.birthday, hFeet=feet, hInches=inches, weight=current_user.weight, gender=current_user.gender)

@main.route('/info', methods=['POST'])
@login_required
def info_post():
    name = request.form.get('name')
    birthday = request.form.get('birthday')
    height = (12 * int(request.form.get('height_feet'))) + int(request.form.get('height_inches'))
    print(height)
    weight = request.form.get('weight')
    gender = request.form.get('gender')
    
    db.session.delete(current_user)
    
    current_user.name = name
    current_user.birthday = birthday
    current_user.height = height
    current_user.weight = weight
    current_user.gender = gender
    
    db.session.add(current_user)
    db.session.commit()
    
    flash('Your changes have been saved!')
    
    return redirect(url_for('main.info'))