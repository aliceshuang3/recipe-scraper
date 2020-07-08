from flask_mail import Message
from flask import render_template
from app import app, mail
from threading import Thread
from app.models import User

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()

def send_password_reset_email(user):
    token = user.get_reset_token()
    send_email('[Novice Chef] Reset Your Password',
               sender=app.config['MAIL_USERNAME'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def email_feedback(name, subject, sender, recipient, feedback_body):
    msg = Message("[Feedback] " + subject, sender=sender, recipients=[recipient])
    msg.body = """
      From: %s <%s>
      Feedback: %s
      """ % (name, sender, feedback_body)
    mail.send(msg)
    Thread(target=send_async_email, args=(app, msg)).start()

