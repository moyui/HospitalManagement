from flask import render_template, redirect, request, url_for, flash
from . import outpatient
from .form import OpExamForm, OpCheckForm
from ..model import OpCheck, OpCheckAfford, OpCheckin, OpCheckinAfford, OpExam, OpExamAfford, OpRecipe, OpRecipeAfford, OutPatientTimetable
from .. import db

# @outpatient.route('/outpatient/checkin', method= ['GET', 'POST'])
# def checkin():
#         if request.method == 'GET':
#                 return render_template('outpatient/checkin.html', form= form)

@outpatient.route('/outpatient/exam', methods= ['GET', 'POST'])
def exam():
        patientexam = OpExam()
        form = OpExamForm()
        if form.validate_on_submit():
                print(form.examitems.data)
                patientexam.id = form.opid.data
                patientexam.examitems = ','.join(form.examitems.data)
                print(patientexam.examitems)
                db.session.add(patientexam)
                db.session.commit()
        return render_template('outpatient/exam.html', form= form)
