from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#db connection
application = Flask(__name__)
application.config['SECRET_KEY'] = 'KEY'
application.config['SQLALCHEMY_DATABASE_URI']="DB"
db = SQLAlchemy(application)
bcrypt = Bcrypt(application)
login_manager = LoginManager(application)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from project import routes