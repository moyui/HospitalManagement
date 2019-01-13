
from flask import render_template, redirect, request, url_for, flash
from . import charges
from .form import PreChargeCheckForm, PreChargePayForm, PreChargeLoginFrom
from ..model import InPatientDeposit, PatientInfo, OpCheckin, BedInfo, Price, Medicine, UserInfo,ExamItem, CheckItem, InPatientTableSet,InPatientCheck, InPatientInspect,InPatientPrescript, InPatientTimeAndBed, Price
from .. import db
from ..decorator import is_login, isauth


@charges.route('/charges', methods=['GET', 'POST'])
@is_login
@isauth
def index(name, auth):
    return render_template('charges/index.html', name=name, auth=auth)


@charges.route('/charges/deposit/check', methods=['GET', 'POST'])
@is_login
@isauth
def depositCheck(name, auth):
    checkForm = PreChargeCheckForm()
    if request.method == 'GET':
        return render_template('charges/depositCheck.html', form=checkForm, name=name, auth=auth)
    else:
        if checkForm.validate_on_submit():
            formPatientId = checkForm.id.data
            # 查找当前最后一条看病记录
            OpCheckInInfo = OpCheckin.query.filter_by(
                patientid=formPatientId, jips=True).order_by(OpCheckin.patientid.desc()).first()
            # 如果病人需要住院
            if OpCheckInInfo:
                return redirect(url_for('.depositPay',  patientid=formPatientId, opcheckid=OpCheckInInfo.opcheckinid))
            else:
                flash('查找不到该病人')
                return render_template('charges/depositCheck.html', form=checkForm, name=name, auth=auth)


@charges.route('/charges/deposit/pay', methods=['GET', 'POST'])
@is_login
@isauth
def depositPay(name, auth):
    patientId = request.args.get('patientid')
    opCheckInId = request.args.get('opcheckid')
    payForm = PreChargePayForm()
    patientInfo = PatientInfo.query.filter_by(id=patientId).first()
    depositInfo = InPatientDeposit.query.filter_by(
        id=opCheckInId, patientid=patientId).order_by(InPatientDeposit.id.desc()).first()
    if request.method == 'GET':
        payForm.id.data = patientId
        payForm.name.data = patientInfo.name
        payForm.age.data = patientInfo.age
        payForm.sex.data = patientInfo.sex
        # 查看剩余押金数
        if depositInfo:
            return render_template('charges/depositPay.html', rest=depositInfo.rest, form=payForm, name=name, auth=auth)
        else:
            return render_template('charges/depositPay.html', rest=0, form=payForm, name=name, auth=auth)
    else:
        if payForm.validate_on_submit():
            # 查询押金表
            if depositInfo:
                oldRest = depositInfo.rest
                depositInfo.rest = oldRest+float(payForm.precharge.data)
                db.session.commit()
            else:
                rest = payForm.precharge.data
                deposit = InPatientDeposit(
                    id=opCheckInId,
                    rest=float(rest),
                    totalcost=0,
                    ischeck=False,
                    patientid=patientId
                )
                db.session.add(deposit)
                db.session.commit()
            flash('金额充值成功')
            return redirect(url_for('.depositPay',  patientid=patientId, opcheckid=opCheckInId))

@charges.route('/charges/pay/check', methods=['GET', 'POST'])
@is_login
@isauth
def payCheck(name, auth):
    form = PreChargeLoginFrom()
    if request.method == 'GET':
        return render_template('charges/payCheck.html', form=form, name=name, auth= auth)
    else:
        formPatientid = form.patientid.data
        depositInfo = InPatientDeposit.query.filter_by(
            patientid=formPatientid, ischeck=False).order_by(InPatientDeposit.id.desc()).first()
        patientInfo = PatientInfo.query.filter_by(id=formPatientid).first()
        if depositInfo and patientInfo:
            form.name.data = patientInfo.name
            form.age.data = patientInfo.age
            form.sex.data = patientInfo.sex
            return redirect('/charges/pay/real?patientid=%s&id=%s'%(formPatientid, depositInfo.id))
        else:
            flash('查找不到该病人')
            return render_template('charges/payCheck.html', form=form, name=name, auth=auth)
    
@charges.route('/charges/pay/real', methods=['GET', 'POST'])
@is_login
@isauth
def payReal(name, auth):
    if request.method == 'GET':
        id = request.args.get('id')
        depositInfo = InPatientDeposit.query.filter_by(
            id=id).order_by(InPatientDeposit.id.desc()).first()
        tableSetInfo = InPatientTableSet.query.filter_by(id=id).first()
        checkInfo = InPatientCheck.query.filter_by(tableid=id).all()
        inspectInfo = InPatientInspect.query.filter_by(tableid=id).all()
        prespectInfo = InPatientPrescript.query.filter_by(tableid=id).all()
        bedInfo = InPatientTimeAndBed.query.filter_by(tableid=id).all()
        
        count = 0
        for i in checkInfo:
            count = count + float(i.cost)
        for i in inspectInfo:
            count = count + float(i.cost)
        for i in prespectInfo:
            count = count + float(i.cost)

        checkItems = []
        inspectItems = []
        prespecItems = []
        bedItems = []

        for i in checkInfo:
            items = i.checkitemsid.split(',')
            doctorid = i.doctorinfoid
            doctorname = UserInfo.query.filter_by(id=doctorid).first().name
            temp = []
            for j in items:
                checkInfo = CheckItem.query.filter_by(
                    id=j).first()
                price = Price.query.filter_by(optionid=int(checkInfo.id)).first()
                temp.append('名称：%s 单价：%s'%(checkInfo.checkitemname, price.price))
            checkItems.append(
                {'id': i.id, 'name': temp, 'doctorname': doctorname, 'cost': i.cost})
        for i in inspectInfo:
            items = i.inspectitemsid.split(',')
            doctorid = i.doctorinfoid
            doctorname = UserInfo.query.filter_by(id=doctorid).first().name
            temp = []
            for j in items:
                inspectInfo = ExamItem.query.filter_by(
                    id=j).first()
                price = Price.query.filter_by(optionid=int(inspectInfo.id)).first()
                temp.append('名称：%s 单价：%s'%(inspectInfo.examitemname, price.price))
            inspectItems.append(
                {'id': i.id, 'name': temp, 'doctorname': doctorname})
        for i in prespectInfo:
            items = i.medicineid.split(',')
            nums = i.medicinenumbers.split(',')
            zipped = zip(items, nums)
            doctorid = i.doctorinfoid
            doctorname = UserInfo.query.filter_by(id=doctorid).first().name
            temp = []
            for j in zipped:
                medicine = Medicine.query.filter_by(
                    id=j[0]).first()
                price = Price.query.filter_by(optionid=int(medicine.id)).first()
                temp.append('名称：%s 数量：%s 单价：%s'%(medicine.medicinename,j[1], price.price))
            prespecItems.append(
                {'id': i.id, 'name': temp, 'doctorname': doctorname})
        for i in bedInfo:
            doctorid = i.doctorinfoid
            doctorname = UserInfo.query.filter_by(id=doctorid).first().name
            bedItems.append({'id': i.id, 'bedid': i.bedid, 'doctorname': doctorname,'startdate': i.startdate, 'enddate': i.enddate})
        
        return render_template('charges/payReal.html', total=count, rest=depositInfo.rest, auth=auth, check=checkItems, persect=prespecItems, inspect=inspectItems, bed=bedItems)

