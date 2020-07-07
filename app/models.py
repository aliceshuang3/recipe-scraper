from datetime import datetime
from app import db, login_manager, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# many to many relationship between users and their saved recipes
saved_recipes = db.Table('saved_recipes',
                    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'))
                    )

# The id field is usually in all models, and is used as the primary key. 
# Each user in the database will be assigned a unique id value, stored in this field. 
# Primary keys are, in most cases, automatically assigned by the database

# Difference between db.String and db.Text: a string field has a limit of 255 characters, 
# whereas a text field has a character limit of 30,000 characters

# User class created below inherits from db.Model, 
# a base class for all models from Flask-SQLAlchemy
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))    
    recipes = db.relationship('Recipe', secondary=saved_recipes, backref='users', lazy='dynamic')

    # to disable concurrent, simultaneous logins per user:
    # when a user logs in, generate a session token and save it in the db
    #session_token = db.Column(db.Text, index=True)

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

    # token expires in 30 minutes
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    # verifies the token
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        # check if the token is invalid/time expired/etc
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        # if we are able to get the user id without getting an exception
        return User.query.get(user_id)
    """
    def __init__(self, username, email, password_hash):
        username = self.username
        email = self.email
        password_hash = self.password_hash
    """
class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.Text)
    recipe_link = db.Column(db.Text)
    image_link = db.Column(db.Text)
    instructions = db.Column(db.Text)
    servings = db.Column(db.Text)
    # one to many relationship between recipe and ingredients
    ingredients = db.relationship("Ingredient", backref='recipe') 

    def __repr__(self):
        return '<Recipe {}>'.format(self.recipe_name)
    """
    def __init__(self, recipe_name, recipe_link, image_link, instructions, servings):
        recipe_name = self.recipe_name
        recipe_link = self.recipe_link
        image_link = self.image_link
        instructions = self.instructions
        servings = self.servings
    """
class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    ingredient_name = db.Column(db.Text)

    def __repr__(self):
        return '<Ingredient {}>'.format(self.ingredient_name)
    """
    def __init__(self, ingredient_name):
        ingredient_name = self.ingredient_name
    """
#Class to add, update and delete data via SQLALchemy sessions
class CRUD():
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()
        
    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()


# Application will configure a user loader function that can be called 
# to load a user given the ID for the Flask-Login extension 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


"""
# Application will configure a user loader function that can be called 
# to load a user given the session token for the Flask-Login extension 
@login.user_loader
def load_user(session_token):                                                                                                                        
    return User.query.filter_by(session_token=session_token).first()
"""


"""
Example usage of database queries
https://www.michaelcho.me/article/many-to-many-relationships-in-sqlalchemy-models-flask
user = User.query.first()
user.recipes.all()  # List all recipes, eg [<recipeA>, <recipeB> ]
user.saved    # List all saved recipes, eg [<saved1>, <saved2>]
user.saved[0].recipes  # List recipes from the first order

p1 = Recipe.query.first()
p1.users  # List all users who have saved this recipe, eg [<user1>, <user2>]

savedrecipesList = user.recipes.all()
for recipe in savedrecipesList:
    print(recipe.recipe_name)
"""