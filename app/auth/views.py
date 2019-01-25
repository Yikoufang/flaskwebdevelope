# -*- coding:utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user,logout_user, login_required, current_user

from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm, InputAccountForm, ResetPasswordForm, ModifyEmailRequestForm
from app import db
from ..email import send_email
from datetime import datetime


@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(url_for('main.index'))
		flash('Invalid username or password.')
	return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('auth.login'))

	
@auth.route('/secret')
@login_required
def secret():
	return 'Only authenticated users are allowed!'

	
@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,
					username=form.username.data,
					password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email, 'Confirm You Account', 'auth/email/confirm', user=user, token=token)
		#flash('You can now login.')
		flash('A confirmation email has been sent to you by email.')
		return redirect(url_for('main.index'))
	return render_template('auth/register.html', form=form)
	

@auth.route('/confirm/<token>')
@login_required       #该修饰符只让已认证用户访问该路由
def confirm(token):    #确认邮件中有该路由的URL地址，点击时访问该路由
	if current_user.confirmed:#current_user是当前登录的用户，未确认的用户该判断跳过，confirmed属性在user.confirm（token）中赋值
		return redirect(url_for('main.index'))
	if current_user.confirm(token):#该方法中赋值confirmed属性，对比令牌id是否与存储在current_user中的已登录用户匹配
		flash('You have confirmed your account.Thanks!')
	else:
		flash('The confirmation link is invalid or has expired.')
	return redirect(url_for('main.index'))


	
@auth.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.ping()
		if not current_user.confirmed \
			and request.endpoint[:5] != 'auth.'\
			and request.endpoint != 'static':	# 冒号为if语句,'\'表示换行
				return redirect(url_for('auth.unconfirmed'))


		
@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
	flash('A new confirmation email has been sent to you by email.')
	return redirect(url_for('main.index'))

	
@auth.route('/password_reset_request', methods=['GET', 'POST'])
def password_reset_request():
	form = InputAccountForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			token = user.generate_reset_token()
			send_email(user.email, 'Reset password', 'auth/email/resetpassword', user=user, token=token)
		flash('A email to reset password has been sent to you by email.')
		return redirect(url_for('auth.login'))
	return render_template('auth/password_reset_request.html', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		if User.reset_password(token, form.newpassword.data):
			db.session.commit()
			flash('You have reset your password!')
			return redirect(url_for('auth.login'))
		else:
			return redirect(url_for('main.index'))
	return render_template('auth/resetpassword.html', form=form)

	
@auth.route('/modify_email_request', methods=['GET','POST'])
@login_required
def modify_email_request():
	form = ModifyEmailRequestForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.password.data):
			new_email = form.new_email.data
			token = current_user.generate_email_request_token(new_email)
			send_email(new_email, 'Confirm your email address', 'auth/email/modify_email_request', user=current_user, token=token)
			flash('An email with instructions to confirm your new email address has been sent to you')
			return redirect(url_for('main.index'))
		else:
			flash('Invalid email or password.')
	return render_template('auth/modify_email_request.html', form=form)

	
@auth.route('/new_email_confirm/<token>')
@login_required
def new_email_confirm(token):
	if current_user.new_email_confirm(token):
		db.session.commit()
		flash('Your email address has been updated.')
	else:
		flash('Invalid request.')
	return redirect(url_for('main.index'))