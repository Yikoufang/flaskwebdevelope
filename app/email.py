# -*- coding:utf-8 -*-
from flask_mail import Message, current_app
from flask import render_template
from . import mail
from manage import app
from threading import Thread

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)
def send_email(to, subject, template, **kwargs):
	msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,sender = current_app.config['FLASKY_MAIL_SENDER'], recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html',**kwargs)#渲染邮件正文的HTML模板，其中**kwargs为传入模板的参数，如user=user，token=token
	thr = Thread(target=send_async_email,args=[app,msg])
	thr.start()
	return thr