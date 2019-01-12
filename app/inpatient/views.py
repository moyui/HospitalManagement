from flask import render_template, redirect, request, url_for, flash
from . import inpatient
from .form import InPatientLoginFrom, InPatientTableSetFrom, InPatientCloseBedForm, InPatientCloseBedForm, InPatientNewBedForm, InPatientInspectForm, InPatientCheckForm, InpatientPrescriptForm
from ..model import InPatientCheck, InPatientInspect, InPatientPrescript, InPatientTableSet, InPatientTimeAndBed, PatientInfo, InPatientDeposit, BedInfo, Price, Medicine
from .. import db
from ..decorator import is_login
import datetime


@inpatient.route('/inpatient', methods=['GET', 'POST'])
@is_login
def index(name):
    form = InPatientLoginFrom()
    if request.method == 'GET':
        return render_template('inpatient/login.html', form=form, name=name)
    else:
        formPatientid = form.patientid.data
        depositInfo = InPatientDeposit.query.filter_by(
            patientid=formPatientid, ischeck=False).order_by(InPatientDeposit.id.desc()).first()
        patientInfo = PatientInfo.query.filter_by(id=formPatientid).first()
        if depositInfo and patientInfo:
            form.name.data = patientInfo.name
            form.age.data = patientInfo.age
            form.sex.data = patientInfo.sex
            return render_template('inpatient/login.html', form=form, patientid=formPatientid, id=depositInfo.id, name=name)
        else:
            flash('查找不到该病人')
            return render_template('inpatient/login.html', form=form, name=name)


@inpatient.route('/inpatient/list', methods=['GET', 'POST'])
@is_login
def patientList(name):
    patientid = request.args.get('patientid')
    id = request.args.get('id')
    return render_template('inpatient/list.html', patientid=patientid, id=id, name=name)


@inpatient.route('/inpatient/registertabset', methods=['GET', 'POST'])
@is_login
def registerTableSet(name):
    patientid = request.args.get('patientid')
    id = request.args.get('id')
    tableSetInfo = InPatientTableSet.query.filter_by(id=id).first()
    form = InPatientTableSetFrom()
    if request.method == 'GET':
        if tableSetInfo:
            checkInfo = InPatientCheck.query.filter_by(tableid=id).all()
            inspectInfo = InPatientInspect.query.filter_by(tableid=id).all()
            prespectInfo = InPatientPrescript.query.filter_by(tableid=id).all()
            return render_template('inpatient/tableset.html', check=checkInfo, persect=prespectInfo, inspect=inspectInfo, name=name, patientid=patientid, id=id)
        else:
            form.id.data = patientid
            return render_template('inpatient/tableset.html', nodata=True, form=form, name=name, patientid=patientid, id=id)
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
        flash('成功添加病人信息套表')
        checkInfo = InPatientCheck.query.filter_by(tableid=id).all()
        inspectInfo = InPatientInspect.query.filter_by(tableid=id).all()
        prespectInfo = InPatientPrescript.query.filter_by(tableid=id).all()
        return redirect('/inpatient/list?patientid=%s&id=%s'%(patientid,id))


@inpatient.route('/inpatient/bed', methods=['GET', 'POST'])
@is_login
def bed(name):
    patientid = request.args.get('patientid')
    id = request.args.get('id')
    myBed = InPatientTimeAndBed.query.filter_by(tableid=id).order_by(InPatientTimeAndBed.id.desc()).first()
    print(myBed)
    if request.method == 'GET':
        return render_template('inpatient/bed/index.html', myBed=myBed, patientid=patientid, id=id, name=name)


@inpatient.route('/inpatient/bed/close', methods=['GET', 'POST'])
@is_login
def closeBed(name):
    patientid = request.args.get('patientid')
    id = request.args.get('id')
    form = InPatientCloseBedForm()
    myBed = InPatientTimeAndBed.query.filter_by(tableid=id).order_by(
        InPatientTimeAndBed.id.desc()).first()
    if request.method == 'GET':
        form.bedId.data = myBed.bedid
        form.startDate.data = myBed.startdate
        form.endDate.data = datetime.datetime.now()
        return render_template('inpatient/bed/closeBed.html', myBed=myBed, form=form, name=name)
    else:
        myBed.enddate = datetime.datetime.now()
        bedtable = BedInfo.query.filter_by(id=myBed.bedid).first()
        bedtable.isused = False
        db.session.commit()
        flash('结束床位成功')
        return redirect('/inpatient/list?patientid=%s&id=%s'%(patientid,id))


@inpatient.route('/inpatient/bed/new', methods=['GET', 'POST'])
@is_login
def newBed(name):
    patientid = request.args.get('patientid')
    id = request.args.get('id')
    form = InPatientNewBedForm()
    doctorid = request.cookies.get('doctorid')
    if request.method == 'GET':
        return render_template('inpatient/bed/newBed.html', form=form, name=name)
    else:
        bed = InPatientTimeAndBed(
            tableid=id,
            bedid=int(form.bedlist.data),
            doctorinfoid=doctorid,
            startdate=datetime.datetime.now(),
            enddate=None
        )
        db.session.add(bed)
        db.session.commit()
        newBedInfo = InPatientTimeAndBed.query.filter_by(tableid=id).order_by(InPatientTimeAndBed.id.desc()).first()
        tableset = InPatientTableSet.query.filter_by(id=id).order_by(
            InPatientTableSet.id.desc()).first()
        inpatienttimeandbedidlist = tableset.inpatienttimeandbedid
        # 如果已有数据
        if (inpatienttimeandbedidlist):
            inpatienttimeandbedidlist = inpatienttimeandbedidlist.split(',')
            inpatienttimeandbedidlist.append(str(newBedInfo.id))
            tableset.inpatienttimeandbedid = ','.join(inpatienttimeandbedidlist)
        else:
            tableset.inpatienttimeandbedid = str(newBedInfo.id)
        bedtable = BedInfo.query.filter_by(id=int(form.bedlist.data)).first()
        bedtable.isused = True
        db.session.commit()
        flash('新建病床成功')
        return redirect('/inpatient/list?patientid=%s&id=%s'%(patientid,id))


@inpatient.route('/inaptient/check', methods=['GET', 'POST'])
@is_login
def check(name):
    patientid = request.args.get('patientid')
    id = request.args.get('id')
    form = InPatientCheckForm()
    doctorid = request.cookies.get('doctorid')
    if request.method == 'GET':
        form.opid.data = id
        return render_template('inpatient/check.html', form=form, name=name)
    else:
        if form.validate_on_submit():
            count = 0
            for i in form.checkitems.data:
                checkinfo = Price.query.filter_by(optionid= int(i)).first()
                count = count + checkinfo.price

            check = InPatientCheck(
                tableid=int(id),
                checkitemsid=','.join(form.checkitems.data),
                doctorinfoid=doctorid,
                cost=count
            )
            db.session.add(check)
            db.session.commit()
            flash('选择的检查项目已经上传')
        return redirect('/inpatient/list?patientid=%s&id=%s'%(patientid,id))

@inpatient.route('/inaptient/inspect', methods=['GET', 'POST'])
@is_login
def inspect(name):
    patientid = request.args.get('patientid')
    id = request.args.get('id')
    form = InPatientInspectForm()
    doctorid = request.cookies.get('doctorid')
    if request.method == 'GET':
        form.opid.data = id
        return render_template('inpatient/inspect.html', form=form, name=name)
    else:
        if form.validate_on_submit():
            count = 0
            for i in form.examitems.data:
                inspectinfo = Price.query.filter_by(optionid= int(i)).first()
                count = count + inspectinfo.price

            inspect = InPatientInspect(
                tableid=int(id),
                inspectitemsid=','.join(form.examitems.data),
                doctorinfoid=doctorid,
                cost=count
            )
            db.session.add(inspect)
            db.session.commit()
            flash('选择的检验项目已经上传')
        return redirect('/inpatient/list?patientid=%s&id=%s'%(patientid,id))

@inpatient.route('/inpatient/recipe', methods=['GET','POST'])
@is_login
def recipe(name):
    patientid = request.args.get('patientid')
    id = request.args.get('id')
    form = InpatientPrescriptForm()
    doctorid = request.cookies.get('doctorid')
    if request.method == 'GET':
        form.opid.data = id
        return render_template('/inpatient/medicine.html', form=form, name=name)
    else:
        if form.validate_on_submit():
            prescript = InPatientPrescript(
                tableid=int(id),
                medicineid=','.join(form.medicines.data),
                medicinenumbers=None,
                doctorinfoid=doctorid,
                cost=None
            )
            db.session.add(prescript)
            db.session.commit()
            return redirect(url_for('inpatient.recipenum', patientid=patientid, id=id))
        
@inpatient.route('/inpatient/recipenum', methods= ['GET', 'POST'])
@is_login
def recipenum(name):
    patientid = request.args.get('patientid')
    id = request.args.get('id')
    form = InpatientPrescriptForm()
    doctorid = request.cookies.get('doctorid')
    medicineInfo = InPatientPrescript.query.filter_by(tableid=id).order_by(InPatientPrescript.id.desc()).first()
    print(medicineInfo)
    if request.method == 'GET':
        form.opid.data = id
        medicineIdList = medicineInfo.medicineid.split(',')
        medicineNameList = []
        for i in medicineIdList:
            med = Medicine.query.filter_by(id=i).first()
            medname = med.medicinename
            medicineNameList.append(medname)
        return render_template('inpatient/recipenum.html', medsnlist= medicineNameList, name=name)
    else:
        mednumbers = []
        d = request.values.to_dict()
        for num in d.keys():
            mednumbers.append(d.get(num))
        medicineInfo.medicinenumbers = ','.join(mednumbers)

        #计算价格
        count = 0
        medicineIdList = medicineInfo.medicineid.split(',')
        zipinfo = zip(medicineIdList, mednumbers)
        for item in zipinfo:
            medinfo = Price.query.filter_by(optionid= int(item[0])).first()
            count = count + medinfo.price * int(item[1])
        medicineInfo.cost = count
        db.session.commit()
        flash('选择的处方已经上传完成')
        return redirect('/inpatient/list?patientid=%s&id=%s'%(patientid,id))
