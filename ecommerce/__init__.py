import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_debug import Debug
from flask_marshmallow import Marshmallow
from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine
#from decimal import *
#from flask_mail import Mail
#from flask_mail import Message



login_manager = LoginManager()

app = Flask(__name__)

# Often people will also separate these into a separate config.py file
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["MONGO_URI"] = "mongodb+srv://reuvenz:ox4MnL8lfZE4tSwx@reuvenz-mongo-xatdp.mongodb.net/reuven-db-1?retryWrites=true&w=majority"
mongo = PyMongo(app)

db2 = MongoEngine(app)

db = SQLAlchemy(app)
Migrate(app,db)
Debug(app)
ma = Marshmallow(app)

'''
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'my_username@gmail.com',
    MAIL_PASSWORD = 'my_password',
))

mail = Mail(app)
msg = Message("Hello",
            sender="from@example.com",
            recipients=["rovenroven1@gmail.com"])

mail.send(msg)
'''

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when Xthey need to login.
login_manager.login_view = "index"
