# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class ModifyPasswordForm(Form):
	oldpassword = PasswordField('old password', validators=[Required()])
	newpassword = PasswordField('confirm new password', validators=[Required()])
	newpassword2 = PasswordField('new password', validators=[Required(),\
								EqualTo('newpassword2',message='password must match')])
	submit = SubmitField('modify')