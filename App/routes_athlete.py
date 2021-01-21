from flask import Flask
from flask import abort, render_template, redirect, request, session, url_for, jsonify, flash
from App import app, models
from flask_login import current_user, login_user, login_required, logout_user

from App import db
from App.models import Coach, Athlete, User, Training, Goal
from App.forms import InformationForm, GoalForm, STYLE_CHOICES, ProgressForm

from datetime import datetime
from calendar import monthrange

@app.route("/athlete")
def athlete():
    goals = Goal.query.filter_by(athlete_id=current_user.id).all()
    return render_template("goal_tracker.html", goals=goals, choices=STYLE_CHOICES)


@app.route('/info', methods=['POST', 'GET'])
def info():
    form = InformationForm()

    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.height = form.height.data
        current_user.weight = form.weight.data
        current_user.birthday = form.birthday.data

        db.session.commit()
        flash('Congratulations, information completed!')
        flash('Add your first GOAL!')
        return redirect(url_for('new_goal'))

    return render_template('form_athlete.html', title='Information', form=form)

@app.route('/goal', methods=['POST', 'GET'])
def new_goal():
    form = GoalForm()

    if form.validate_on_submit():
        goal = Goal(athlete_id=current_user.id, style=form.style.data, deadline=form.deadline.data,
                        distance=form.distance.data, time=form.time.data)

        db.session.add(goal)
        db.session.commit()
        flash('Congratulations, new goal added!')
        return redirect(url_for('athlete'))

    return render_template('form_athlete.html', title='Goal', form=form)

@app.route('/update_goal', methods=['POST', 'GET'])
def update_goal():
    id = request.args.get('id')

    form = ProgressForm()

    if form.validate_on_submit():
        goal = Goal.query.filter_by(athlete_id=current_user.id, id=id).first()
        goal.progress = form.progress.data

        if(goal.progress != 0):
            if( (goal.time / goal.progress * 100) > 100 ):
                goal.achieved = True
                goal.deadline = datetime.now()
        

        db.session.commit()
        flash('Goal was updated sucessfully!')
        return redirect(url_for('athlete'))

    return render_template('form_athlete.html', title='Goal', form=form)

@app.route('/athlete_calendar')
def athlete_calendar():
    # list with range number of days of the current month
    days = list(
        range(1, monthrange(datetime.now().year, datetime.now().month)[1]+1))
    # date of the fisrt day of the current month
    date = "1" + " " + str(datetime.now().month) + \
        " " + str(datetime.now().year)
    # week number for the first day of the month
    week_day = datetime.strptime(date, '%d %m %Y').weekday()
    skip_days = list(range(0, week_day))

    trainings = Training.query.all()
    trainings_days = []
    for training in trainings:
        if training.start_date.month == datetime.now().month:
            trainings_days.append(training.start_date.day)

    return render_template("athlete_calendar.html", today=datetime.now(), days=days, skip_days=skip_days, trainings=trainings_days)