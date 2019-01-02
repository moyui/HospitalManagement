from flask import render_template, redirect, request, url_for, flash
from . import inpatient
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from .form import InPatientLoginFrom, InPatientTimeAndBed
from ..model import InPatientCheck, InPatientInspect, InPatientPrescript, InPatientTableSet, InPatientTimeAndBed, PatientInfo
from .. import db

@inpatient.route('/inpatient', methods=['GET', 'POST'])
def index():
    form = InPatientLoginFrom()
    if request.method == 'GET':
        return render_template('inpatient/login.html', form=form)
    else:
        formPatientid = form.patientid.data
        inPatientInfo = PatientInfo.query.filter_by(id=formPatientid).first()
        if inPatientInfo:
            name = inPatientInfo.name
            age = inPatientInfo.age
            sex = inPatientInfo.sex
            return render_template('inpatient/login.html', form=form, patientid=formPatientid, age=age, name=name, sex=sex)
        else:
            return render_template('inpatient/login.html', form=form, nodata=True)


@inpatient.route('/inpatient/<id>/bed', methods=['GET', 'POST'])
def bed():
    form = InPatientTimeAndBed()
    if request.method == 'GET':
        return render_template('inpatient/bed.html', form=form)
    else:
        bedTableid = InPatientTableSet.query.filter_by(
            id=id).first().inpatienttimeandbedid
        InPatientTimeAndBed.query.filter_by(id=bedTableid).first().update({
            'badid': form.data.badId,
            'startdate': form.data.startDate,
            'enddate': form.data.endDate
        })
        return redirect('/inpatient/<id>')
=======
from .form import PreChargeForm
from .model import InPatientCheck, InPatientInspect, InPatientPrescript, InPatientTableSet, InPatientTimeAndBed
=======
from .form import InPatientLoginFrom
=======
from .form import InPatientLoginFrom, InPatientTimeAndBed
>>>>>>> add running
from ..model import InPatientCheck, InPatientInspect, InPatientPrescript, InPatientTableSet, InPatientTimeAndBed, PatientInfo
>>>>>>> add:增加部分住院代码
from .. import db


@inpatient.route('/inpatient', methods=['GET', 'POST'])
def index():
    form = InPatientLoginFrom()
    if request.method == 'GET':
        return render_template('inpatient/login.html', form=form)
    else:
        formPatientid = form.patientid.data
        if formPatientid is not None:
            inPatientInfo = PatientInfo.query.filter_by(
                id=formPatientid).first()
            name = inPatientInfo.name
            age = inPatientInfo.age
            sex = inPatientInfo.sex

            return render_template('inpatient/login.html', form=form, patientid=formPatientid, age=age, name=name, sex=sex)
        else:
            return render_template('inpatient/login.html', nodata=true)


<<<<<<< HEAD

    inPatient = InPatientTableSet.query.filter_by(patientid=patientid and close=False).first()
    if inpatient is not None:
        return redirect
>>>>>>> add:住院收费与住院部分开发
=======
@inpatient.route('/inpatient/<id>/bed', methods=['GET', 'POST'])
def bed():
    form = InPatientTimeAndBed()
    if request.method == 'GET':
        return render_template('inpatient/bed.html', form=form)
    else:
        bedTableid = InPatientTableSet.query.filter_by(
            id=id).first().inpatienttimeandbedid
        InPatientTimeAndBed.query.filter_by(id=bedTableid).first().update({
            'badid': form.data.badId,
            'startdate': form.data.startDate,
            'enddate': form.data.endDate
        })
        return redirect('/inpatient/<id>')
<<<<<<< HEAD
>>>>>>> add:增加部分住院代码
=======
>>>>>>> add running
