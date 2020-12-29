from flask import Flask
from flask import abort, render_template, redirect, request, session, url_for, jsonify, flash
from App import app, models
from flask_login import current_user, login_user, login_required, logout_user

from App import db
from App.models import Coach, Athlete, User
from App.forms import LoginForm, RegistrationForm, ROLE_CHOICES, InformationForm


@app.route("/coach")
def coach():
    return render_template("dashboard.html")

@app.route('/athletes')
def athletes():

    athletes = Athlete.query.join(Coach,
        Coach.coach_id == Athlete.coach_id).filter(Athlete.coach_id==current_user.coach_id)

    return render_template("athletes.html", athletes=athletes)
