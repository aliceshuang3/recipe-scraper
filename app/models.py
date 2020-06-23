from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# The id field is usually in all models, and is used as the primary key. 
# Each user in the database will be assigned a unique id value, stored in this field. 
# Primary keys are, in most cases, automatically assigned by the database

# User class created below inherits from db.Model, 
# a base class for all models from Flask-SQLAlchemy
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    recipes = db.relationship('Recipe', backref='client', lazy='dynamic')
    # to disable concurrent, simultaneous logins per user:
    # when a user logs in, generate a session token and save it in the db
    #session_token = db.Column(db.String(40), index=True)

    def __repr__(self):
        # if we did User.query.get(some id #), we would get the <User username>
        return '<User {}>'.format(self.username)  
    # functions to hash the password and a verification function
    # it returns True if the password provided by the user matches the hash, or False otherwise. 
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    # returns session token instead of user ID
    #def get_id(self):                                                           
    #    return str(self.session_token) 

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String())
    # timestamp useful for retrieving posts in chronological order
    # working with UTC dates and times in a server application because it ensures 
    # that you are using uniform timestamps regardless of where the users are located. 
    # These timestamps will be converted to the user's local time when they are displayed.
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Recipe {}>'.format(self.body)


# Application will configure a user loader function that can be called 
# to load a user given the ID for the Flask-Login extension 
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
"""
# Application will configure a user loader function that can be called 
# to load a user given the session token for the Flask-Login extension 
@login.user_loader
def load_user(session_token):                                                                                                                        
    return User.query.filter_by(session_token=session_token).first()
"""