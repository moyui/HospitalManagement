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
    # if form.validate_on_submit():
    #     user = User

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterFrom()
    if form.validate_on_submit():
        user = UserInfo(
            idcard = form.idcard.data,
            name = form.name.data,
            password = form.password.data,
            groupid = form.role.data
        )
        db.session.add(user)
        
