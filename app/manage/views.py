# -*- coding:utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from . import manage
from flask_login import login_user,logout_user, login_required, current_user
from ..models import User
from .forms import ModifyPasswordForm
from app import db

@manage.route('/modifypassword', methods=['GET', 'POST'])
@login_required
def modifypassword():
	form = ModifyPasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.oldpassword.data):
			current_user.password=form.newpassword.data
			db.session.add(current_user)
			db.session.commit()
			flash('You have changed your password!')
			return redirect(url_for('main.index'))
	return render_template('manage/modifypassword.html', form=form)