# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')
	
class RegistrationForm(Form):
	email = StringField('Email', validators=[Required(), Length(1,64), Email()])
	username = StringField('Usernme', validators=[
		Required(), Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
		'Username must have only letters, numbers, dots or underscores')])
	password = PasswordField('Password', validators=[
		Required(), EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('Register')
	
	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')
			
	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')

class InputAccountForm(Form):
	email = StringField('Enter your email please', validators=[Required(), Length(1,64), Email()])
	submit = SubmitField('submit')
	
class ResetPasswordForm(Form):
	username = StringField('Username',validators=[Required(), Length(1,64), Email()])#还需要输入么？
	newpassword = PasswordField('new password', validators=[Required()])
	newpassword2 = PasswordField('confirm new password', validators=[Required(),\
								EqualTo('newpassword2',message='password must match')])
	submit = SubmitField('submit')
	
class ModifyEmailRequestForm(Form):
	new_email = StringField('New email', validators=[Required(), Length(1,64), Email()])
	password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('submit')
	
	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')