from flask import render_template, redirect, request, url_for, flash
from . import charges
from .form import PreChargeForm
from .model import InPatientDeposit, InPatientTotalCost
from .. import db

@charges.route('/charges/deposit/<id>', methods=['GET', 'POST'])
def getDeposit(id):
    form = PreChargeForm()
    if form.validate_on_submit():
        deposit = InPatientDeposit(
            patientid = id,
            rest = form.precharge.data
        )
        totalCost = InPatientTotalCost(
            patientid = id,
            totalcost = 0
        )
        db.session.add(deposit)
        db.session.add(totalCost)
        db.session.commit()
        return redirect(url_for(''))
    return render_template('changes/deposit.html', form=form)
