import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # The first term looks for the value of an environment variable, also called SECRET_KEY. 
    # The second term, is just a hardcoded string
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False