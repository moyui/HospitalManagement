from flask import render_template, redirect, request, url_for, flash
from . import inpatient
from .form import InPatientLoginFrom, InPatientTableSetFrom, InPatientBedForm
from ..model import InPatientCheck, InPatientInspect, InPatientPrescript, InPatientTableSet, InPatientTimeAndBed, PatientInfo, InPatientDeposit, BedInfo
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
