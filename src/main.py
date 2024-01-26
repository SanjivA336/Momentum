from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import User, UserData, Exercises, History, Days
from sqlalchemy import or_
from . import db

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
@login_required
def home():
    return render_template('main/home.html', path=request.path)

@main.route('/info')
@login_required
def info():
    name = current_user.name
    birthday = getAttribute("birthday")
    height = getAttribute("height")
    weight = getAttribute("weight")
    gender = getAttribute("gender")

    feet = ""
    inches = ""
    if(height != None):
        feet = int(height) // 12
        inches = int(height) % 12

    return render_template('profile/info.html', name=name, birthday=birthday, hFeet=feet, hInches=inches, weight=weight, gender=gender)

@main.route('/info', methods=['POST'])
@login_required
def info_post():
    name = request.form.get('name')
    birthday = request.form.get('birthday')
    height = ((12 * int(request.form.get('height_feet'))) + int(request.form.get('height_inches')))
    weight = request.form.get('weight')
    gender = request.form.get('gender')
    
    updateAttribute("birthday", birthday)
    updateAttribute("height", height)
    updateAttribute("weight", weight)
    updateAttribute("gender", gender)

    db.session.delete(current_user)
    current_user.name = name
    db.session.add(current_user)
    db.session.commit()
    
    flash('Your changes have been saved!')
    
    return redirect(url_for('main.info'))

@main.route('/preferences')
@login_required
def prefs():
    cycle = getCycle()
    return render_template('profile/prefs.html', name=current_user.name, cycle=cycle)

@main.route('/edit', methods=['POST'])
@login_required
def edit_post():
    dayNum = int(request.form.get('edit'))
    print(dayNum)
    day = getDay(dayNum)
    options = Exercises.query.filter(or_(isverified=True, creator_id=current_user.id)).all()

    return render_template('profile/edit.html', name=current_user.name, day=day, options=options)

@main.route('/settings')
@login_required
def settings():
    return render_template('profile/settings.html', name=current_user.name)




def updateAttribute(attribute_name, attribute_value):
    attribute_id = removeIfAttributeExists(attribute_name)
    if(attribute_id == "DNE"):
        attribute = UserData(user_id=current_user.id, attribute_name=attribute_name, attribute_value=attribute_value)
    else:
        attribute = UserData(attribute_id=attribute_id, user_id=current_user.id, attribute_name=attribute_name, attribute_value=attribute_value)

    db.session.add(attribute)
    db.session.commit()

def removeIfAttributeExists(attribute_name):
    attribute = getAttribute(attribute_name)
    if(attribute != None):
        id = attribute.attribute_id
        db.session.delete(attribute)
        db.session.commit()
        return id
    return "DNE"

def getAttribute(attribute_name):
    attribute = UserData.query.filter_by(user_id=current_user.id, attribute_name=attribute_name).first()
    if(attribute != None):
        return attribute.attribute_value
    return None

def getCycle():
    numDays = getAttribute("num_days_in_cycle")
    if(numDays == None):
        updateAttribute("num_days_in_cycle", 0)
        numDays = 0

    cycle = []
    for i in range(1, int(numDays) + 1):
        day = getDay(i)
        if(day == None):
            updateDay(i, "Day " + str(i), 0, 0, 0, 0, 0, 0)
            day = getDay(i)
        cycle.append([i, day[2], [getExercise(day.exercise_id_1).name, getExercise(day.exercise_id_2).name, getExercise(day.exercise_id_3).name, getExercise(day.exercise_id_4).name, getExercise(day.exercise_id_5).name, getExercise(day.exercise_id_6).name]])
    return cycle

def updateDay(dayNumber, name, exercise_id_1, exercise_id_2, exercise_id_3, exercise_id_4, exercise_id_5, exercise_id_6):
    day_id = removeIfDayExists(dayNumber)
    if(day_id == "DNE"):
        day = Days(user_id=current_user.id, name=name, day_in_cycle=dayNumber, exercise_id_1=exercise_id_1, exercise_id_2=exercise_id_2, exercise_id_3=exercise_id_3, exercise_id_4=exercise_id_4, exercise_id_5=exercise_id_5, exercise_id_6=exercise_id_6)
    else:
        day = Days(day_id=day_id, user_id=current_user.id, name=name, day_in_cycle=dayNumber, exercise_id_1=exercise_id_1, exercise_id_2=exercise_id_2, exercise_id_3=exercise_id_3, exercise_id_4=exercise_id_4, exercise_id_5=exercise_id_5, exercise_id_6=exercise_id_6)

    db.session.add(day)
    db.session.commit()

def removeIfDayExists(dayNumber):
    day = getDay(dayNumber)
    if(day != None):
        id = day.day_id
        db.session.delete(day)
        db.session.commit()
        return id
    return "DNE"

def getDay(dayNumber):
    dayQuery = Days.query.filter_by(user_id=current_user.id, day_in_cycle=dayNumber).first()
    day = [dayQuery.day_id, dayQuery.user_id, dayQuery.name, dayQuery.day_in_cycle, [dayQuery.exercise_id_1, dayQuery.exercise_id_2, dayQuery.exercise_id_3, dayQuery.exercise_id_4, dayQuery.exercise_id_5, dayQuery.exercise_id_6]]
    return day

def getExercise(exercise_id):
    exercise = Exercises.query.filter_by(exercise_id=exercise_id).first()
    return exercise


class Day:
    def __init__(self, user_id, day_in_cycle):
        query = Days.query.filter_by(user_id=user_id, day_in_cycle=day_in_cycle).first()
        if(query != None):
            self.day_id = query.day_id
            self.user_id = query.user_id
            self.name = query.name
            self.day_in_cycle = query.day_in_cycle
            self.exercise_ids = [query.exercise_id_1, query.exercise_id_2, query.exercise_id_3, query.exercise_id_4, query.exercise_id_5, query.exercise_id_6]
        else:
            day = Days(user_id=current_user.id, name="Day " + str(day_in_cycle), day_in_cycle=day_in_cycle, exercise_id_1=0, exercise_id_2=0, exercise_id_3=0, exercise_id_4=0, exercise_id_5=0, exercise_id_6=0)
            db.session.add(day)
            db.session.commit()
            self.day_id = day.day_id
            self.user_id = day.user_id
            self.name = day.name
            self.day_in_cycle = day.day_in_cycle
            self.exercise_ids = [day.exercise_id_1, day.exercise_id_2, day.exercise_id_3, day.exercise_id_4, day.exercise_id_5, day.exercise_id_6]

    def update(self, name, exercise_id_1, exercise_id_2, exercise_id_3, exercise_id_4, exercise_id_5, exercise_id_6):
        self.name = name
        self.exercise_ids = [exercise_id_1, exercise_id_2, exercise_id_3, exercise_id_4, exercise_id_5, exercise_id_6]
    
    def getExercise(self, order):
        return getExercise(self.exercise_ids[order - 1])
    

    
        