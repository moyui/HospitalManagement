from flask import render_template, redirect, request, url_for, flash, make_response
from . import auth
from .form import LoginForm, RegisterFrom
from ..model import UserInfo
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('auth/login.html', form=form)
    else:
        if form.validate_on_submit():
            user = UserInfo.query.filter_by(id=form.id.data).first()
            if user:
                response = make_response(redirect('/'))
                response.set_cookie('doctorid', user.id)
                response.set_cookie('doctorname', user.name)
                return response
            else:
                return render_template('auth/login.html', form=form, nodata=True)
    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    response = make_response(redirect('/'))
    response.delete_cookie('doctorid')
    response.delete_cookie('doctorname')
    return response


@auth.route('/register', methods=['GET', 'POST'])  # 这块代码暂时放弃
def register():
    form = RegisterFrom()
    if form.validate_on_submit():
        user = UserInfo(
            id=form.id.data,
            name=form.name.data,
            sex=form.name.sex,
            password=form.password.data,
            groupid=form.role.data,
            rank=form.rank.data
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('anth/register.html', form=form)
