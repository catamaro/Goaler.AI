from App import app, login
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import with_polymorphic, relationship, backref, foreign
from App.database import Base

from datetime import datetime
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


@login.user_loader
def load_user(id):
    coach = app.session.query(Coach).get(int(id))
    if coach is not None:
        return coach
    else:
        return app.session.query(Athlete).get(int(id))

class User(UserMixin, Base):
    __tablename__ = 'user'
    # attributes of the class
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))
    
    def __repr__(self):
        return '<User: {} -> Email: {}>'.format(self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Coach(User):
    __tablename__ = 'coach'

    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'coach',
                        'inherit_condition': (id == User.id)}

    coach_id = Column(String(8), primary_key=True, unique=True)
    athletes = relationship('Athlete', primaryjoin="(Coach.coach_id==Athlete.coach_id)", backref=backref('coach'), lazy='dynamic') 

    def __repr__(self):
        return("{}({!r} {!r} {!r})".format(self.__class__.__name__, self.username, self.email, self.coach_id ))

class Athlete(User):
    __tablename__='athlete'

    id=Column(Integer, ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'athlete',
                        'inherit_condition': (id == User.id)}

    coach_id=Column(Integer, ForeignKey('coach.coach_id'))