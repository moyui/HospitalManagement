from flask import render_template, redirect, request, url_for, flash
from . import inpatient
from .form import PreChargeForm
from .model import InPatientCheck, InPatientInspect, InPatientPrescript, InPatientTableSet, InPatientTimeAndBed
from .. import db

@inpatient.route('/inpatient', methods=['GET', 'POST'])
def index():
    form = 


    inPatient = InPatientTableSet.query.filter_by(patientid=patientid and close=False).first()
    if inpatient is not None:
        return redirect