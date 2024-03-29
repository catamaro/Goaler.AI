from flask import Flask, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = 'login' # redirect to login endpoint when not loggin

bootstrap = Bootstrap(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from App import routes_athlete, routes_coach, routes, models, forms