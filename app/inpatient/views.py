from flask import render_template, redirect, request, url_for, flash
from . import inpatient
from .form import InPatientLoginFrom, InPatientTableSetFrom, InPatientCloseBedForm, InPatientCloseBedForm, InPatientNewBedForm
from ..model import InPatientCheck, InPatientInspect, InPatientPrescript, InPatientTableSet, InPatientTimeAndBed, PatientInfo, InPatientDeposit, BedInfo
from .. import db
import datetime


@inpatient.route('/inpatient', methods=['GET', 'POST'])
def index():
    form = InPatientLoginFrom()
    if request.method == 'GET':
        return render_template('inpatient/login.html', form=form)
    else:
        formPatientid = form.patientid.data
        depositInfo = InPatientDeposit.query.filter_by(
            patientid=formPatientid, ischeck=False).order_by(InPatientDeposit.id.desc()).first()
        patientInfo = PatientInfo.query.filter_by(id=formPatientid).first()
        if depositInfo and patientInfo:
            name = patientInfo.name
            age = patientInfo.age
            sex = patientInfo.sex
            return render_template('inpatient/login.html', form=form, patientid=formPatientid, id=depositInfo.id)
        else:
            return render_template('inpatient/login.html', form=form, nodata=True)


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
            inpatienttimeandbedid=None,
            inpatientcheckid=None,
            inpatientinspectid=None,
            inpatientprescriptid=None
        )
        db.session.add(tableset)
        db.session.commit()
        return redirect('')


@inpatient.route('/inpatient/bed', methods=['GET', 'POST'])
def bed():
    patientid = request.args.get('patientid')
    id = request.args.get('id')
    remainBed = BedInfo.query.filter_by(isused=False).all()
    myBed = InPatientTimeAndBed.filter_by(tableid=id).order_by(
        InPatientTimeAndBed.id.desc()).first()
    if request.method == 'GET':
        return render_template('inpatient/bed/index.html', myBed=myBed, patientid=patientid, id=id)


@inpatient.route('/inpatient/bed/close', methods=['GET', 'POST'])
def closeBed():
    patientid = request.args.get('patientid')
    id = request.args.get('id')
    form = InPatientCloseBedForm()
    myBed = InPatientTimeAndBed.filter_by(tableid=id).order_by(
        InPatientTimeAndBed.id.desc()).first()
    if request.method == 'GET':
        form.bedId.data = myBed.bedid
        form.startDate.data = myBed.startdate
        form.endDate.date = datetime.datetime.now()
        return render_template('inpatient/bed/closeBed.html',
                               myBed=myBed, form=form)
    else:
        myBed.update({
            'enddate': form.endDate.data
        })
        bedtable = BedInfo.filter_by(id=myBed.bedid).first()
        bedtable.update({
            'isused': False
        })
        return redirect('')


@inpatient.route('/inpatient/bed/new', methods=['GET', 'POST'])
def newBed():
    patientid = request.args.get('patientid')
    id = request.args.get('id')
    form = InPatientNewBedForm()
    remainBed = BedInfo.query.filter_by(isused=False).all()
    if request.method == 'GET':
        return render_template('inpatient/bed/newBed.html', form=form, remainBed=remainBed)
    else:
        bed = InPatientTimeAndBed(
            id='',  # 自增字段
            tableid=id,
            bedid=form.bedId.data,
            doctorinfoid='',  # cookie登录态
            startdate=datetime.datetime.now(),
            enddate=None
        )
        db.session.add(bed)
        db.commit()
        newBedInfo = InPatientTimeAndBed.query(tableid=id).order_by(
            InPatientTimeAndBed.id.desc()).first()
        tableset = InPatientTableSet.query(id=id).order_by(
            InPatientTableSet.id.desc()).first()
        tableset.update({
            'inpatienttimeandbedid': tableset.inpatienttimeandbedid + ',' + newBedInfo.id
        })
        bedtable = BedInfo.filter_by(id=form.bedId.data).first()
        bedtable.update({
            'isused': True
        })
        return redirect('')
