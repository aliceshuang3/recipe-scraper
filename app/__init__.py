from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# users can log in to the application and then navigate to 
# different pages while the application "remembers" that the user is logged in
from flask_login import LoginManager
from flask_mail import Mail
# send errors by email
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

app = Flask(__name__)
# tell Flask to read config file and apply it
app.config.from_object(Config)

# database objects must be created after the application
# database initialization
db = SQLAlchemy(app)
# database migration engine instantiation
migrate = Migrate(app, db)

# login extension created/initialized after app instantiation
# feature that  forces users to log in before 
# they can view certain pages of the application
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# for resetting passwords
mail = Mail(app)

# Logging errors by email
# only going to enable the email logger when the app is running without debug mode
def create_app(config_class=Config):
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['MAIL_USERNAME'], subject='Novice Chef Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
        
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            # rotates the logs ensuring that log files do not grow too large when the app runs for a long time
            file_handler = RotatingFileHandler('logs/novicechef.log', maxBytes=10240, backupCount=10)
            # timestamp, logging level, the message and the source file and line number from where the log entry originated
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Novice Chef startup')
return app
# models is a module that will define the structure of the database
# import error handlers
from app import routes, models, errors

