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
        return("{}({!r} {!r} {!r} {!r} {!r})".format(self.__class__.__name__, self.username, self.email, self.height, self.weight, self.birthday ))


class Training(db.Model):
    __tablename__='training'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    training_type = db.Column(db.Integer)
        
    def __repr__(self):
            return("{}({!r} {!r} {!r})".format(self.__class__.__name__, self.start_date, self.end_date, self.training_type ))

class Swimming(db.Model):
    __tablename__='swimming'

    id = db.Column(db.Integer, primary_key=True)
    warm_up = db.Column(db.PickleType)
    workout = db.Column(db.PickleType)
    cool_down = db.Column(db.PickleType)
    train_type = db.Column(db.String)

    def __repr__(self):
            return("{}({!r} {!r} {!r})".format(self.__class__.__name__, self.warm_up, self.workout, self.cool_down ))

class Event(db.Model):
    __tablename__='events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    event_type = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    def __repr__(self):
            return("{}({!r} {!r} {!r} {!r})".format(self.__class__.__name__, self.name, self.event_type, self.start_date, self.end_date ))


class Goal(db.Model):
    __tablename__='goal'
    
    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer)
    style = db.Column(db.String)
    distance = db.Column(db.Integer)
    deadline = db.Column(db.DateTime)
    achieved = db.Column(db.Boolean, default=False)
    time = db.Column(db.Float)
    progress = db.Column(db.Float, default=0)

    def __repr__(self):
            return("{}({!r} {!r} {!r} {!r} {!r} {!r} {!r})".format(self.__class__.__name__, self.athlete_id, self.style, self.distance, self.time, self.deadline, self.achieved, self.progress))