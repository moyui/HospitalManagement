from flask import render_template, redirect, request, url_for, flash
from . import inpatient
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from .form import InPatientLoginFrom, InPatientTimeAndBed
from ..model import InPatientCheck, InPatientInspect, InPatientPrescript, InPatientTableSet, InPatientTimeAndBed, PatientInfo
=======
from .form import InPatientLoginFrom, InPatientTableSetFrom, InPatientBedForm
from ..model import InPatientCheck, InPatientInspect, InPatientPrescript, InPatientTableSet, InPatientTimeAndBed, PatientInfo, InPatientDeposit, BedInfo
>>>>>>> add 住院部分
from .. import db


@inpatient.route('/inpatient', methods=['GET', 'POST'])
def index():
    form = InPatientLoginFrom()
    if request.method == 'GET':
        return render_template('inpatient/login.html', form=form)
    else:
        formPatientid = form.patientid.data
        # depositInfo = InPatientDeposit.query.filter_by(
        #     patientid=formPatientid, ischeck=False).order_by(InPatientDeposit.id.desc()).first()
        # patientInfo = PatientInfo.query.filter_by(id=formPatientid).first()
        # if depositInfo and patientInfo:
        #     name = patientInfo.name
        #     age = patientInfo.age
        #     sex = patientInfo.sex
        #     return render_template('inpatient/login.html', patientid=formPatientid, id=depositInfo.id)
        # else:
        #     return render_template('inpatient/login.html', form=form, nodata=True)
        return render_template('inpatient/login.html', patientid=1, id=22, form=form)


@inpatient.route('/inpatient/list', methods=['GET', 'POST'])
def patientList():
    patientid = request.args.get('patientid')
    id = request.args.get('id')
    return render_template('inpatient/list.html', patientid=patientid, id=id)


@inpatient.route('/inpatient/registertabset', methods=['GET', 'POST'])
def registerTableSet():
    patientid = request.args.get('patientid')
    id = request.args.get('id')
    tableSetInfo = InPatientTableSet.query.filter_by(id=id).first()
    form = InPatientTableSetFrom()
    if request.method == 'GET':
        if tableSetInfo:
            checkInfo = InPatientCheck.query.filter_by(tableid=id).all()
            inspectInfo = InPatientInspect.query.filter_by(tableid=id).all()
            prespectInfo = InPatientPrescript.query.filter_by(tableid=id).all()
            return render_template('inpatient/tableset.html', check=checkInfo, persect=prespectInfo, inspect=inspectInfo)
        else:
            return render_template('inpatient/tableset.html', nodata=True, form=form)
    else:
        tableset = InPatientTableSet(
            id=id,
            inpatienttimeandbedid='',
            inpatientcheckid='',
            inpatientinspectid='',
            inpatientprescriptid=''
        )
        db.session.add(tableset)
        db.session.commit()
        return redirect('')


@inpatient.route('/inpatient/bed', methods=['GET', 'POST'])
def bed():
    patientid = request.args.get('patientid')
    id = request.args.get('id')
    form = InPatientTimeAndBed()
    remainBed = BedInfo.query.filter_by(isused=False).all()
    myBed = InPatientTimeAndBed.filter_by(tableid=id).order_by(InPatientTimeAndBed.id.desc()).first()
    if request.method == 'GET':
        return render_template('inpatient/bed/index.html', form=form, remainBed = remainBed, myBed=myBed)
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
