from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
SECRET_KEY=os.urandom(12).hex()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///register.db?check_same_thread=False'
app.config['SECRET_KEY'] =SECRET_KEY
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login=LoginManager(app)
from user import routes