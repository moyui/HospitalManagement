
from flask import render_template, redirect, request, url_for, flash
from . import charges
from .form import PreChargeCheckForm, PreChargePayForm
from ..model import InPatientDeposit, PatientInfo, OpCheckin
from .. import db
from ..decorator import is_login


@charges.route('/charges', methods=['GET', 'POST'])
@is_login
def index(name):
    return render_template('charges/index.html', name=name)


@charges.route('/charges/deposit/check', methods=['GET', 'POST'])
@is_login
def depositCheck(name):
    checkForm = PreChargeCheckForm()
    if request.method == 'GET':
        return render_template('charges/depositCheck.html', form=checkForm, name=name)
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
                return render_template('charges/depositCheck.html', form=checkForm, name=name)


@charges.route('/charges/deposit/pay', methods=['GET', 'POST'])
@is_login
def depositPay(name):
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
            return render_template('charges/depositPay.html', rest=depositInfo.rest, form=payForm, name=name)
        else:
            return render_template('charges/depositPay.html', rest=0, form=payForm, name=name)
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
