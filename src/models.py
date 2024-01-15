from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(1000))
    name = db.Column(db.String(100))
    admin = db.Column(db.Boolean, default=False)
    
class UserData(UserMixin, db.Model):
    attribute_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    attribute_name = db.Column(db.String(100))
    attribute_value = db.Column(db.String(100))
    
class Exercises(UserMixin, db.Model):
    exercise_id = db.Column(db.Integer, primary_key=True)
    verified = db.Column(db.Boolean, default=True)
    name = db.Column(db.String(100))
    muscle_group = db.Column(db.String(100))
    
class History(UserMixin, db.Model):
    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    date = db.Column(db.Date)
    day_in_cycle = db.Column(db.Integer)
    exercise_id = db.Column(db.Integer)
    exercise_metric = db.Column(db.Integer)
    set_number = db.Column(db.Integer)
    
class Days(UserMixin, db.Model):
    day_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    day_in_cycle = db.Column(db.Integer)
    exercise_id_1 = db.Column(db.Integer)
    exercise_id_2 = db.Column(db.Integer)
    exercise_id_3 = db.Column(db.Integer)
    exercise_id_4 = db.Column(db.Integer)
    exercise_id_5 = db.Column(db.Integer)
    exercise_id_6 = db.Column(db.Integer)
