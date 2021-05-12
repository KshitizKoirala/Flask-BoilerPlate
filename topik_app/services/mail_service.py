from threading import Thread
from flask_mail import Message
from flask import current_app

# Initialized Mail Extension
from topik_app.extensions import mail


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except ConnectionRefusedError:
            raise InternalServerError("[MAIL SERVER] not working.")


def send_mail(subject, sender, recipients, text_body, html_body):
    app = current_app._get_current_object()
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()
