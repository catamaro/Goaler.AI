from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, DateField, FloatField
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
        user = app.session.query(User).filter(
            User.username == username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = app.session.query(User).filter(
            User.email == email.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class InformationForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    birthday = DateField('Birthday Date (yyyy-MM-DD)')
    height = FloatField('Height')
    weight = FloatField('Weight')
    submit = SubmitField('Save')

