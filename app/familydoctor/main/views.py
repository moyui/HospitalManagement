from flask import render_template, session, redirect, url_for, current_app, abort, flash, request, current_app
from datetime import datetime
from flask_login import login_required, current_user

from . import main
from .forms import Nameform, EditProfileForm, EditProfileAdminForm, PostForm
from .. import db
from ..models import User, Role, Post, Permission
from ..email import send_email
from ..dacorators import admin_required

#首页路由
@main.route('/', methods=['GET', 'POST'])
def index():
    # form = Nameform()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.name.data).first()
    #     if user is None:
    #         user = User(username=form.name.data)
    #         db.session.add(user)
    #         session['known'] = False
    #         if current_app.config['FLASKY_ADMIN']:
    #             send_email(current_app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
    #     else:
    #         session['known'] = True
    #     session['name'] = form.name.data
    #     return redirect(url_for('.index'))
    # return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow())
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        #当前用户应该有撰写博文的权限才能书写博文
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))#蓝本为'index'这个视图函数加上了一个为main的命名空间，所以其路径其实是main.index，而不像单文本程序时的路径index
        #.index属于简写，请求所在的蓝本，而跨蓝本重定向则一定要使
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, pagination=pagination)

#用户资料路由
@main.route('/user/<username>')
def user(username):
#     user = User.quert.filter_by(username=username).first()
#     if user is None:
#         abort(404)
#     return render_template('user.html', user=user)
    user = User.query.filter_by(username=username).first_or_404()
    # posts = user.posts.order_by(Post.timestamp.desc()).all()
    # return render_template('user.html', user=user, posts=posts)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts, pagination=pagination)

#用户资料编辑路由
@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('你的资料已经得到更新。')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    #在打开资料编辑页面时，form.validate_on_submit()因为没有提交任何更改，所以说，它一定会返回false，即
    #接下来的编辑操作均不执行，在false的同时，就会执行下面三行，通过current_user的属性给表单赋予初值，而当
    #用户修改过自己的资料之后，提交的时候form.validate_on_submit()才会True，即执行编辑操作，并提交数据库更改
    return render_template('edit_profile.html', form=form)

#管理员编辑用户资料路由
@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required#在只有验证用户可以访问的同时，还应该被管理员验证装饰器检查
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('你的资料已经得到更新。')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
#整体逻辑与用户资料编辑相同

@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMIN):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('博文已经进行了更新。')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)