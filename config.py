import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # The first term looks for the value of an environment variable, also called SECRET_KEY. 
    # The second term, is just a hardcoded string
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # Suppress deprecation warning   
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = os.environ.get('recipe_email_username')
    MAIL_PASSWORD = os.environ.get('recipe_email_password')