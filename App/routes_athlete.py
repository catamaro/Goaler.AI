from flask import Flask
from flask import abort, render_template, redirect, request, session, url_for, jsonify, flash
from App import app, models
from flask_login import current_user, login_user, login_required, logout_user

from App import db
from App.models import Coach, Athlete, User
from App.forms import InformationForm


@app.route("/athlete")
def athlete():
    return render_template("goal_tracker.html")


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
        return redirect(url_for('athlete'))

    return render_template('form.html', title='Information', form=form)
