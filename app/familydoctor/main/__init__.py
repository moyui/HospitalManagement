#由蓝本定义的路由，在蓝本被注册到程序中去之前，是处于休眠的，而被注册时，路由才成为程序的一部分，解决了路由创建时间的冲突
from flask import Blueprint

main = Blueprint('main', __name__)#设定蓝本的名称

from .import views, errors#避免循环导入，在路由views和errors中还要导入蓝本main
from ..models import Permission

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)