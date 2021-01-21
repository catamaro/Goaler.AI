from flask import Flask
from flask import abort, render_template, redirect, request, session, url_for, jsonify, flash
from App import app, models
from flask_login import current_user, login_user, login_required, logout_user

from App import db
from App.models import Coach, Athlete, User, Training, Swimming, Event, Goal
from App.forms import TrainingForm, EventForm, EVENT_CHOICES

from datetime import datetime
from calendar import monthrange


@app.route("/coach")
def coach():
    events = Event.query.all()
    goals = Goal.query.all()
    athletes = Athlete.query.all()

    return render_template("dashboard.html", events=events, choices=EVENT_CHOICES, goals=goals, athletes=athletes)


@app.route('/athletes')
def athletes():
    athletes = Athlete.query.join(Coach,
                                  Coach.coach_id == Athlete.coach_id).filter(Athlete.coach_id == current_user.coach_id)

    return render_template("athletes.html", athletes=athletes)


@app.route('/planing')
def planing():

    """ Swimming.query.delete()
    db.session.commit() """
    options = Swimming.query.all()

    if not options:
        warm_up = {"Swim freestyle":"1 x 400m, 30s rest", "Swim freestyle":"4 x 100m, 30s rest", 
                    "Freestyle pull":"1 x 300m, 20s rest", "Freestyle kick":"1 x 300m, 20s rest"}
        workout = {"Freestyle kick":"1 x 400m, 30s rest", "Swim freestyle":"4 x 100m, 30s rest", 
                    "Freestyle pull":"1 x 300m, 20s rest", "Freestyle kick":"1 x 300m, 20s rest"}
        cool_down = {"Slow swimming":"1 x 100m"}
        train_type = "Max Speed"
        option1 = Swimming(warm_up=warm_up, workout=workout, cool_down=cool_down, train_type=train_type)

        warm_up = {"Swim freestyle":"1 x 75m, 20s rest, repeat 3x", "Fast free kick":"1 x 25m, 20s rest, repeat 3x", 
                    "Backstroke kick":"1 x 75m, 20s rest, repeat 3x", "Fast backstroke kick":"1 x 25m, 20s rest, repeat 3x"}
        workout = {"Freestyle kick":"1 x 400m, 30s rest", "Swim freestyle":"4 x 100m, 30s rest", 
                    "Freestyle pull":"1 x 300m, 20s rest", "Freestyle kick":"1 x 300m, 20s rest"}
        cool_down = {"Slow swimming":"1 x 100m"}
        train_type = "Accelaration"
        option2 = Swimming(warm_up=warm_up, workout=workout, cool_down=cool_down, train_type=train_type)

        warm_up = {"Swim freestyle":"1 x 400m, 30s rest", "Swim freestyle":"4 x 100m, 30s rest", 
                    "Freestyle pull":"1 x 300m, 20s rest", "Freestyle kick":"1 x 300m, 20s rest"}
        workout = {"Freestyle kick":"1 x 400m, 30s rest", "Swim freestyle":"4 x 100m, 30s rest", 
                    "Freestyle pull":"1 x 300m, 20s rest", "Freestyle kick":"1 x 300m, 20s rest"}
        cool_down = {"Slow swimming":"1 x 100m"}
        train_type = "Personalized"
        option3 = Swimming(warm_up=warm_up, workout=workout, cool_down=cool_down, train_type=train_type)

        db.session.add(option1)
        db.session.add(option2)
        db.session.add(option3)
        db.session.commit()

        options = Swimming.query.all()

    trainings = Training.query.all()
    return render_template("plans.html", trainings=trainings, options = options)

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
        if training.start_date.month == datetime.now().month:
            trainings_days.append(training.start_date.day)

    return render_template("calendar.html", today=datetime.now(), days=days, skip_days=skip_days, trainings=trainings_days)


@ app.route("/new_training", methods=['GET', 'POST'])
def new_training():

    form = TrainingForm()
    if form.validate_on_submit():

        start_date = datetime(form.date.data.year, form.date.data.month, 
                            form.date.data.day, form.start_hour.data.hour, form.start_hour.data.minute)
        end_date = datetime(form.date.data.year, form.date.data.month, 
                            form.date.data.day, form.end_hour.data.hour, form.end_hour.data.minute)

        train = Training(start_date=start_date, end_date=end_date, 
                            training_type=form.training_type.data)

        db.session.add(train)
        db.session.commit()
        flash('New training was registered!')
        return redirect(url_for('calendar'))

    return render_template('form_coach.html', title='New Training', form=form)


@ app.route("/new_event", methods=['GET', 'POST'])
def new_event():

    form = EventForm()
    if form.validate_on_submit():

        start_date = datetime(form.start_date.data.year, form.start_date.data.month, 
                            form.start_date.data.day)
        end_date = datetime(form.end_date.data.year, form.end_date.data.month, 
                            form.end_date.data.day)

        event = Event(name=form.name.data, start_date=start_date, end_date=end_date, 
                            event_type=form.event_type.data)

        db.session.add(event)
        db.session.commit()
        flash('New event was registered!')
        return redirect(url_for('coach'))

    return render_template('form_coach.html', title='New Event', form=form)
