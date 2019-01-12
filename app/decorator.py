from functools import wraps
from flask import redirect, request

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