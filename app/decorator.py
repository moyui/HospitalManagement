from functools import wraps
from flask import redirect, request
from .model import UserInfo

def is_login(f):
    @wraps(f)#保证被装饰的函数依然保有原函数名，而不会因为装饰而导致变为decorated_function
    def decorated_function(*args, **kwargs):
        doctorinfoid = request.cookies.get('doctorid')
        if doctorinfoid or request.path == '/' or request.path == '/login':
            doctorname = request.cookies.get('doctorname')
            return f(name=doctorname, *args, **kwargs)
        else: 
            return redirect('/')
    return decorated_function

def isauth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        doctorinfoid = request.cookies.get('doctorid')
        if doctorinfoid:
            d = {}
            userinfo = UserInfo.query.filter_by(id= doctorinfoid).first()
            d['ismenzhen'] = userinfo.ismenzhen
            d['iszhuyuan'] = userinfo.iszhuyuan
            d['isjiating'] = userinfo.isjiating
            d['isjizhen'] = userinfo.isjizhen
            d['isshoufei'] = userinfo.isshoufei
            d['isguahao'] = userinfo.isguahao
            return f(auth= d, *args, **kwargs)
        else:
            return f(auth= {}, *args, **kwargs)
    return decorated_function