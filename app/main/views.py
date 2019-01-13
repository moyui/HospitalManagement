from flask import render_template, redirect, request, url_for, flash
from .form import Exit, PatientInfoForm
from . import main
from ..model import PatientInfo
from ..decorator import is_login, isauth
from .. import db

@main.route('/', methods=['GET', 'POST'])
@is_login
@isauth
def index(name, auth):
    return render_template('/welcome.html', name=name, auth= auth)

@main.route('/patientinfo', methods= ['GET', 'POST'])
@is_login
@isauth
def patientinfo(name, auth):
    form = PatientInfoForm()
    patientinfo = PatientInfo()
    if request.method == 'GET':
        return render_template('/patientinfo.html', form= form, auth= auth, name= name)
    else:
        patientinfo.id = form.patientid.data
        patientinfo.name = form.name.data
        patientinfo.birth = form.birth.data
        patientinfo.sex = form.sex.data
        patientinfo.age = int(form.age.data)
        
        db.session.add(patientinfo)
        db.session.commit()
        flash('病人信息已经录入')
        return redirect(url_for('outpatient.checkin', patientid= form.patientid.data))