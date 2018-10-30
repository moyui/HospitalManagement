from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm

#处理未认证账户路由
@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()#如果当前用户是已经授权的，那么就调用数据库User模型中ping方法来刷新last_seen属性
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
                #请求的端点不在认证蓝本中
            return redirect(url_for('auth.unconfirmed'))

#处理未认证账户路由——转至未确认页面
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

#登录路由
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()#创建了一个LoginForm对象，来自forms.py，其中也包含了所有该如何渲染页面的表单规则
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)#调用该方法，实现“记住我”，form.remember_me.data返回的是布尔值
            next = request.args.get('next')#涉及到Post/重定向/GET模式，如果用户访问未授权的URL则会显示登录表单，通过request.args可以获取到源地址
            if next is None or not next.startswith('/'):#而当地址不存在或者不以/为开头时，则重定向至首页
                next = url_for('main.index')
            return redirect(next)
        flash('无效的用户名或密码。')
    return render_template('auth/login.html', form=form)#此处将form传给模板，由模板来渲染表单以及页面

#登出路由
@auth.route('/logout')
@login_required#必须先登录才能退出，用login_required来保护该路由，不能在登录前访问该路由
def logout():
    logout_user()
    flash('你已经登出了。')
    return redirect(url_for('main.index'))

#注册路由
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        #user是User类的一个实例
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()#调用类中方法生成令牌
        send_email(user.email, '确认你的账户',
                   'auth/email/confirm', user=user, token=token)#调用扩展方法发送电子邮件
        flash('一封确认邮件已经发到您的邮箱中。')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

#确认路由
@auth.route('/confirm/<token>')
@login_required#只能让认证用户访问，保护该路由，所以当用户点击确认链接后，会跳转回登录页面要求登录，才能执行该函数
def confirm(token):
    #如果已经确认过，那么就将直接跳转到首页
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    #如果确认函数通过，因为调用的是模型中的confirm函数，此时若通过其中的confirmed值已经置为True，只等待上传，那么这时上传即可
    if current_user.confirm(token):
        db.session.commit()
        flash('你已经完成了账户确认，谢谢！')
    else:
        flash('该确认连接不合法或者已经失效。')
    return redirect(url_for('main.index'))

#重发确认路由
@auth.route('/confirm')
@login_required#已登录但是还未确认的用户会触发这个路由，而未登录是不会触发该路由的
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认你的账户',
               'auth/email/confirm', user=current_user, token=token)
    #使用current_user/email确保该路由只会被认证用户触发，并且程序知道该用户是谁
    flash('一封新的确认邮件已经发到您的邮箱中。')
    return redirect(url_for('main.index'))