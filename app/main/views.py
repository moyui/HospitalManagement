from flask import render_template, redirect, request, url_for
from .form import Exit
from . import main
from ..decorator import is_login

@main.route('/', methods=['GET', 'POST'])
@is_login
def index(name):
    return render_template('/base.html', name=name)
