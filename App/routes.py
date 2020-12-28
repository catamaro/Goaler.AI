from flask import Flask
from flask import _app_ctx_stack, abort, render_template, redirect, request, session, url_for, jsonify, flash
from App import app, models
from flask_login import current_user, login_user, login_required, logout_user

from App.database import SessionLocal, engine
from App.models import Coach, Athlete, User
from App.forms import LoginForm, RegistrationForm, ROLE_CHOICES
from sqlalchemy.orm import scoped_session

models.Base.metadata.create_all(bind=engine)

app.session = scoped_session(
    SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
app.session.expire_on_commit = False


@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html")
    else:
        return render_template("landing_page.html")

@app.route("/test")
def test():
    return render_template("index2.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = app.session.query(User).filter(
            User.username == form.username.data).first()
        app.session.close()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        if int(form.role.data) == 0:
            user = Coach(username=form.username.data,
                         email=form.email.data, coach_id=form.coach_id.data)
            print(user.coach_id)
        else:   
            coach = app.session.query(Coach).filter(
                Coach.coach_id == form.coach_id.data).first()
            print(coach)
            if coach is not None:
                user = Athlete(username=form.username.data,
                               email=form.email.data, coach=coach)
            else:
                flash('Error, coach code is not valid')
                return redirect(url_for('register'))

        user.set_password(form.password.data)
        app.session.add(user)
        app.session.commit()
        app.session.close()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/athletes')
def athletes():
    
    athletes = app.session.query(Athlete).join( Coach, 
            Coach.coach_id==Athlete.coach_id).filter(Athlete.coach_id == current_user.coach_id)


    return render_template("athletes.html", athletes=athletes)
    
