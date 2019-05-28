from app import mail
from flask_mail import Message
from threading import Thread
from flask import current_app

#线程处理函数
def send_fun(app, msg) :
    with app.app_context():
        mail.send(msg)

def send_mail(subject, sender, recvers, body, html) :
    msg = Message(subject, sender = sender, recipients = recvers)
    msg.html = html
    msg.body = body
    #创建新线程
    thread = Thread(target=send_fun, args=[current_app._get_current_object(), msg])
    thread.start()