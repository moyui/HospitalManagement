from flask import render_template, redirect, request, url_for
from .form import Exit
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    doctorinfoid = request.cookies.get('doctorid')
    if doctorinfoid:
        doctorname = request.cookies.get('doctorname')
        if request.method == 'GET':
            return render_template('/base.html', name=doctorname)
        else:
            response = make_response('delete cookie')
            response.delete_cookie('doctorid')
            response.delete_cookie('doctorname')
            return render_template('/base.html')
    return render_template('/base.html')
