from flask import Flask
from flask import abort, render_template, redirect, request, session, url_for, jsonify, flash
from App import app, models
from flask_login import current_user, login_user, login_required, logout_user

from App import db
from App.models import Coach, Athlete, User, Training
from App.forms import TrainingForm

from datetime import datetime
from calendar import monthrange


@app.route("/coach")
def coach():
    return render_template("dashboard.html")


@app.route('/athletes')
def athletes():

    athletes = Athlete.query.join(Coach,
                                  Coach.coach_id == Athlete.coach_id).filter(Athlete.coach_id == current_user.coach_id)

    return render_template("athletes.html", athletes=athletes)


@app.route('/calendar')
def calendar():
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
        if training.date.month == datetime.now().month:
            trainings_days.append(training.date.day)

    return render_template("calendar.html", today=datetime.now(), days=days, skip_days=skip_days, trainings=trainings_days)


@ app.route("/new_training", methods=['GET', 'POST'])
def new_training():

    form = TrainingForm()
    if form.validate_on_submit():

        date = datetime(form.date.data.year, form.date.data.month, 
                            form.date.data.day, form.hour.data.hour, form.hour.data.minute)

        train = Training(date=date, duration=form.duration.data, 
                            training_type=form.training_type.data)

        db.session.add(train)
        db.session.commit()
        flash('New training was registered!')
        return redirect(url_for('calendar'))

    return render_template('form_coach.html', title='New Training', form=form)
