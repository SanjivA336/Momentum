from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import MySQLdb.cursors
from . import mysql


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    
    return render_template('auth/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT password FROM users WHERE email = %s', (email, ))
    actualPasswordHash = cursor.fetchone().get('password')

    print(password)
    print(actualPasswordHash)

    if check_password_hash(actualPasswordHash, password):
        print("SUCESS")
        #login_user(user, remember=remember)
        return redirect(url_for('main.profile'))
    else:
        print("FAIL")
        flash('Incorrect Email/Password. Please check your login details and try again')
        return redirect(url_for('auth.login'))

@auth.route('/signup')
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    
    return render_template('auth/signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256')
    birthday = request.form.get('birthday')
    height = request.form.get('height')
    weight = request.form.get('weight')
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email, ))
    user = cursor.fetchone()
    
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    elif not name or not email or not password or not birthday or not height or not weight:
        flash('Please fill out all fields')
        return redirect(url_for('auth.signup'))
        
    cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s, %s)', (email, password, name, birthday, height, weight, ))
    mysql.connection.commit()
    
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))