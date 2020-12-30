from App import app, login
from sqlalchemy.orm import with_polymorphic, relationship, backref, foreign
from App import db

from datetime import datetime
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    coach = Coach.query.get(int(id))
    if coach is not None:
        return coach
    else:
        return Athlete.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    # attributes of the class
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    
    def __repr__(self):
        return '<User: {} -> Email: {}>'.format(self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Coach(User):
    __tablename__ = 'coach'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'coach',
                        'inherit_condition': (id == User.id)}

    coach_id = db.Column(db.String(8), primary_key=True, unique=True)
    athletes = db.relationship('Athlete', primaryjoin="(Coach.coach_id==Athlete.coach_id)", backref=backref('coach'), lazy='dynamic') 

    def __repr__(self):
        return("{}({!r} {!r} {!r})".format(self.__class__.__name__, self.username, self.email, self.coach_id ))

class Athlete(User):
    __tablename__='athlete'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'athlete',
                        'inherit_condition': (id == User.id)}

    coach_id = db.Column(db.Integer, db.ForeignKey('coach.coach_id'))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    birthday = db.Column(db.DateTime)

    def __repr__(self):
        return("{}({!r} {!r} {!r})".format(self.__class__.__name__, self.username, self.email, self.height, self.weight, self.birthday ))


class Training(db.Model):
    __tablename__='training'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    date = db.Column(db.DateTime)
    duration = db.Column(db.Float)
    training_type = db.Column(db.Integer)
        
    def __repr__(self):
            return("{}({!r} {!r} {!r})".format(self.__class__.__name__, self.date, self.duration, self.training_type ))
