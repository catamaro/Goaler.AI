from flask import Flask, request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = 'login' # redirect to login endpoint when not loggin

bootstrap = Bootstrap(app)

from App import database, routes, models, forms