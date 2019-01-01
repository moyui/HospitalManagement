from flask import render_template, redirect, request, url_for, flash
from . import inpatient
from .form import InPatientLoginFrom
from ..model import InPatientCheck, InPatientInspect, InPatientPrescript, InPatientTableSet, InPatientTimeAndBed, PatientInfo
from .. import db

@inpatient.route('/inpatient', methods=['GET', 'POST'])
def index():
    form = InPatientLoginFrom()
    if request.method = 'GET':
        return render_template('inpatient/login.html', form=form)
    else:
        formPatientid = form.patientid.data
        if formPatientid is not None:
            inPatientInfo = PatientInfo.query.filter_by(id=formPatientid).first()
            name = inPatientInfo.name
            age = inPatientInfo.age
            sex = inPatientInfo.sex
            
            return render_template('inpatient/login.html', form=form, patientid = formPatientid, age = age, name = name, sex = sex, age = age)

@inpatient.route('/inpatient/<id>/bed', methods=['GET', 'POST'])
def bed():
    form = InPatientTimeAndBed()
    if request.method = 'GET':
        ('inpatient/bed.html', form=form)
    else:
        bedTableid = InPatientTableSet.query.filter_by(id = id).first().inpatienttimeandbedid
        InPatientTimeAndBed.query.filter_by(id = bedTableid).first().update({
            'badid': form.data.badId,
            'startdate': form.data.startDate
            'enddate': form.data.endDate
        })
        return redirect('/inpatient/<id>')