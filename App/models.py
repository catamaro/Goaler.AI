from App import app, login
from sqlalchemy import Column, Integer, String, DateTime
from App.database import Base

from datetime import datetime
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
    return query(User).get(int(id))

class User(UserMixin, Base):
    __tablename__ = 'User'
    # attributes of the class
    id = Column(Integer, primary_key = True)
    username = Column(String(64), index = True, unique = True)
    email = Column(String(120), index = True, unique = True)
    password_hash =Column(String(128))
    role = Column(Integer)
    last_seen = Column(DateTime, default=datetime.utcnow)

    # method to print the object
    def __repr__(self):
        return '<User: {} -> Email: {}>'.format(self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
