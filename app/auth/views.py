from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .form import LoginForm, RegisterFrom
from ..model import UserInfo
from .. import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if next is None or next.startswith('/'):
                next = url_for('main.index')
            
            return redirect(next)
        flash('无效的用户名或密码。')
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterFrom()
    if form.validate_on_submit():
        user = UserInfo(
            id = form.id.data,
            name = form.name.data,
            sex = form.name.sex,
            password = form.password.data,
            groupid = form.role.data,
            rank = form.rank.data
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('anth/register.html', form=form)
