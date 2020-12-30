from flask import Flask
from flask import abort, render_template, redirect, request, session, url_for, jsonify, flash
from App import app, models
from flask_login import current_user, login_user, login_required, logout_user

from App import db
from App.models import Coach, Athlete, User
from App.forms import LoginForm, RegistrationForm


@app.route("/home")
def home():
    return render_template("landing_page.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        coach = Coach.query.filter_by(id=current_user.id).first()
        athlete = Athlete.query.filter_by(id=current_user.id).first()

        if athlete is not None:
            if current_user.first_name is None:
                flash('Complete your profile')
                return redirect(url_for('info'))
            else:
                return redirect(url_for('athlete'))

        elif coach is not None:
            return redirect(url_for('coach'))

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        if int(form.role.data) == 0:
            user = Coach(username=form.username.data,
                         email=form.email.data, coach_id=form.coach_id.data)
            print(user.coach_id)
        else:
            coach = Coach.query.filter_by(coach_id=form.coach_id.data).first()
            if coach is not None:
                user = Athlete(username=form.username.data,
                               email=form.email.data, coach=coach)
            else:
                flash('Error, coach code is not valid')
                return redirect(url_for('register'))

        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('form.html', title='Register', form=form)
