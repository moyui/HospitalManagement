from flask import render_template, redirect, request, url_for, flash
from . import charges
from .form import PreChargeCheckForm, PreChargePayForm
from ..model import InPatientDeposit, PatientInfo, OpCheckin
from .. import db


@charges.route('/charges/deposit/<id>', methods=['GET', 'POST'])
def getDeposit(id):
    form = PreChargeForm()
    if form.validate_on_submit():
        deposit = InPatientDeposit(
            patientid=id,
            rest=form.precharge.data
        )
        totalCost = InPatientTotalCost(
            patientid=id,
            totalcost=0
        )
        db.session.add(deposit)
        db.session.add(totalCost)
        db.session.commit()
        return redirect(url_for(''))
    return render_template('changes/deposit.html', form=form)


@charges.route('/charges', methods=['GET', 'POST'])
def index():
    return render_template('charges/index.html')


@charges.route('/charges/deposit/check', methods=['GET', 'POST'])
def depositCheck():
    checkForm = PreChargeCheckForm()
    if request.method == 'GET':
        return render_template('charges/depositCheck.html', form=checkForm)
    else:
        if checkForm.validate_on_submit():
            formPatientId = checkForm.id.data
            # 查找当前最后一条看病记录
            OpCheckInInfo = OpCheckin.query.filter_by(
                patientid=formPatientId, jips=True).order_by(OpCheckin.patientid.desc()).first()
            # 如果病人需要住院
            if OpCheckInInfo:
                return redirect(url_for('.depositPay',  patientid=formPatientId, opcheckid=OpCheckInInfo.id))
            else:
                return render_template('charges/depositCheck.html', nodata=True, form=checkForm)


@charges.route('/charges/deposit/pay', methods=['GET', 'POST'])
def depositPay():
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
            return render_template('charges/depositPay.html', rest=depositInfo.rest, form=payForm)
        else:
            return render_template('charges/depositPay.html', rest=0, form=payForm)
    else:
        if payForm.validate_on_submit():
            # 查询押金表
            if depositInfo:
                oldRest = depositInfo.rest
                depositInfo.update({
                    'rest': oldRest+float(payForm.precharge.data)
                })
            else:
                deposit = InPatientDeposit(
                    id=opCheckInId,
                    rest=0,
                    totalcost=0,
                    ischeck=False
                )
                db.session.add(deposit)
                db.session.commit()
            return redirect('')
