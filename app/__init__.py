from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# users can log in to the application and then navigate to 
# different pages while the application "remembers" that the user is logged in
from flask_login import LoginManager

app = Flask(__name__)

# tell Flask to read config file and apply it
app.config.from_object(Config)

# database objects must be created after the application
# database instantiation
db = SQLAlchemy(app)
# database migration engine instantiation
migrate = Migrate(app, db)

# login extension created/initialized after app instantiation
login = LoginManager(app)

# feature that  forces users to log in before 
# they can view certain pages of the application
login = LoginManager(app)
login.login_view = 'login'

# models is a module that will define the structure of the database
from app import routes, models

