from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import SelectField, IntegerField, DateField, FloatField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from App.models import User
from App import app


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


ROLE_CHOICES = [('0', 'Coach'), ('1', 'Athlete')]


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    # uses a stock validator Email() to check format
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # to avoid typos, extra security
    password_repeat = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])

    role = SelectField(u'Role', choices=ROLE_CHOICES)
    coach_id = StringField('Coach Code')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class InformationForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    birthday = DateField('Birthday Date (mm-dd-yyyy)')
    height = FloatField('Height')
    weight = FloatField('Weight')
    submit = SubmitField('Save')

TRAINING_CHOICES = [('0', 'Cardio'), ('1', 'Strength')]

class TrainingForm(FlaskForm):
    date = DateField('Day (mm-dd-yyyy)')
    start_hour = TimeField('Start Hour (hh:mm)', format='%H:%M')
    end_hour = TimeField('End Hour (hh:mm)', format='%H:%M')
    training_type = SelectField(u'Type', choices=TRAINING_CHOICES)
    submit = SubmitField('Save')

EVENT_CHOICES = [('0', 'Regional'), ('1', 'Nacional'), ('2', 'European'), ('3', 'World Championship'), ('4', 'Olympics')]

class EventForm(FlaskForm):
    name = StringField('Event Name')    
    event_type = SelectField(u'Event Type', choices=EVENT_CHOICES)
    start_date = DateField('Start Day (mm-dd-yyyy)')
    end_date = DateField('End Day (mm-dd-yyyy)')
    submit = SubmitField('Save')

STYLE_CHOICES = [('0', 'Freestyle'), ('1', 'Backstroke'), ('2', 'Breaststroke'), ('3', 'Butterfly'), ('4', 'Sidestroke')]

class GoalForm(FlaskForm):
    time = FloatField('Time Goal')    
    distance = IntegerField('Distance')    
    style = SelectField(u'Style', choices=STYLE_CHOICES)
    deadline = DateField('Deadline (mm-dd-yyyy)')
    submit = SubmitField('Save')

class ProgressForm(FlaskForm):
    progress = FloatField('New Record')
    submit = SubmitField('Save')