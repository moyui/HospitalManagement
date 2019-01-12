from flask import render_template, redirect, request, url_for, flash, make_response
from . import outpatient
from .form import OpCheckForm, OpCheckinForm, OpExamForm, OpRecipeForm, OpIndexFrom
from ..model import OpCheck, OpCheckAfford, OpCheckin, OpCheckinAfford, OpExam, OpExamAfford, OpRecipe, OpRecipeAfford, Medicine, Price, UserInfo, OpCost
from .. import db
from ..decorator import is_login
import datetime

@outpatient.route('/outpatient/checkin', methods= ['GET', 'POST'])
@is_login
def checkin(name):
        patientcheckin = OpCheckin()
        form = OpCheckinForm()
        price = OpCheckinAfford()
        if request.method == 'GET':
                return render_template('outpatient/checkin.html', form= form, name= name)
        else:
                if form.validate_on_submit():
                        response = make_response(redirect(url_for('outpatient.opindex', name= name)))
                        prepatient = OpCheckin.query.order_by(OpCheckin.opcheckinid.desc()).first()
                        patientcheckin.opcheckinid = prepatient.opcheckinid + 1

                        nowpcheckid = patientcheckin.opcheckinid
                        response.set_cookie('nopcid', str(nowpcheckid))

                        patientcheckin.patientid = form.patientid.data
                        patientcheckin.doctorid = form.doctorname.data
                        docid = UserInfo.query.filter_by(id= form.doctorname.data).first()
                        patientcheckin.doctortype = docid.rank
                        patientcheckin.jips = False

                        price.opcheckinid = patientcheckin.opcheckinid
                        price.opid = form.patientid.data
                        priceinfo = Price.query.filter_by(optionid= docid.rank).first()
                        price.price = priceinfo.price

                        db.session.add(patientcheckin)
                        db.session.add(price)
                        db.session.commit()

                        return response
                        # print(nowpcheckid)
                        # return redirect(url_for('outpatient.opindex'))
        

@outpatient.route('/outpatient/opindex', methods= ['GET', 'POST'])
@is_login
def opindex(name):
        form = OpIndexFrom()
        nowpcheckid = int(request.cookies.get('nopcid'))
        if request.method == 'GET':
                # nowpcheckid = request.cookies.get('nopcid')
                # print('2', type(int(nowpcheckid)), int(nowpcheckid))
                return render_template('outpatient/opindex.html', form= form, name= name)
        else:
                if form.inpatientcheck.data == True:
                        opcheckininfo = OpCheckin.query.filter_by(opcheckinid= nowpcheckid).first()
                        opcheckininfo.jips = True
                        db.session.commit()
                else :
                        pass
                return render_template('outpatient/opindex.html', form= form, name= name)

@outpatient.route('/outpatient/exam', methods= ['GET', 'POST'])
@is_login
def exam(name):
        patientexam = OpExam()
        form = OpExamForm()
        price = OpExamAfford()
        nowpcheckid = request.cookies.get('nopcid')
        if request.method == 'GET':
                return render_template('outpatient/exam.html', form= form, name= name)
        else:
                if form.validate_on_submit():
                        patientexam.opcheckinid = int(nowpcheckid)
                        patientexam.opid = form.opid.data
                        patientexam.examitems = ','.join(form.examitems.data)

                        price.opcheckinid = patientexam.opcheckinid
                        price.opid = form.opid.data
                        count = 0
                        for item in form.examitems.data:
                                examinfo = Price.query.filter_by(optionid= int(item)).first()
                                count = count + examinfo.price
                        price.price = count

                        db.session.add(patientexam)
                        db.session.add(price)
                        db.session.commit()
                        flash('选择的检验项目已经上传')
                        return redirect(url_for('outpatient.opindex', name= name))
        

@outpatient.route('/outpatient/check', methods= ['GET', 'POST'])
@is_login
def check(name):
        patientcheck = OpCheck()
        form = OpCheckForm()
        price = OpCheckAfford()
        nowpcheckid = request.cookies.get('nopcid')
        if request.method == 'GET':
                return render_template('outpatient/check.html', form= form, name= name)
        else:
                if form.validate_on_submit():
                        patientcheck.opcheckinid = int(nowpcheckid)
                        patientcheck.opid = form.opid.data
                        patientcheck.checkitems = ','.join(form.checkitems.data)

                        price.opcheckinid = patientcheck.opcheckinid
                        price.opid = form.opid.data
                        count = 0
                        for item in form.checkitems.data:
                                checkinfo = Price.query.filter_by(optionid= int(item)).first()
                                count = count + checkinfo.price
                        price.price = count

                        db.session.add(patientcheck)
                        db.session.add(price)
                        db.session.commit()
                        flash('选择的检查项目已经上传')
                        return redirect(url_for('outpatient.opindex', name= name))
        

@outpatient.route('/outpatient/recipe', methods= ['GET', 'POST'])
@is_login
def recipe(name):
        patientrecipe=OpRecipe()
        form = OpRecipeForm()
        nowpcheckid = request.cookies.get('nopcid')
        if request.method == 'GET':
               return render_template('/outpatient/medicine.html', form= form, name= name)
        else: 
                if form.validate_on_submit():
                        patientrecipe.opcheckinid = int(nowpcheckid)
                        patientrecipe.opid = form.opid.data
                        patientrecipe.medicinenames = ','.join(form.medicines.data)
                        db.session.add(patientrecipe)
                        db.session.commit()
                        return redirect(url_for('outpatient.recipenum', name= name))

@outpatient.route('/outpatient/recipenum', methods= ['GET', 'POST'])
@is_login
def recipenum(name):
        nowpcheckid = request.cookies.get('nopcid')
        price = OpRecipeAfford()
        if request.method == 'GET':
                patientcheckinid = int(nowpcheckid)
                selectedinfo = OpRecipe.query.filter_by(opcheckinid= patientcheckinid).first()
                medicinenames = selectedinfo.medicinenames
                medslist = medicinenames.split(',')
                medsnlist = []
                for item in medslist:
                        med = Medicine.query.filter_by(id= item).first()
                        medname = med.medicinename
                        medsnlist.append(medname)
                return render_template('outpatient/recipenum.html', medsnlist= medsnlist, name= name)
        else:
                patientcheckinid = int(nowpcheckid)
                oprecipe = OpRecipe.query.filter(OpRecipe.opcheckinid == patientcheckinid).first()
                mednumbers = []
                d = request.values.to_dict()
                for number in d.keys():
                        mednumbers.append(d.get(number))
                oprecipe.medicinenumbers = ','.join(mednumbers)
                db.session.commit()

                price.opcheckinid = patientcheckinid
                opreinfo = OpRecipe.query.filter_by(opcheckinid= patientcheckinid).first()
                price.opid = opreinfo.opid
                recipeinfo = OpRecipe.query.filter_by(opcheckinid= patientcheckinid).first()
                recipemdname = recipeinfo.medicinenames
                recipemdnamel = recipemdname.split(',')
                recipenum = recipeinfo.medicinenumbers
                recipenuml = recipenum.split(',')
                count = 0
                zipinfo = zip(recipemdnamel, recipenuml)
                for item in zipinfo:
                        medinfo = Price.query.filter_by(optionid= int(item[0])).first()
                        count = count + medinfo.price * int(item[1])
                # for item in recipemdnamel:
                #         medinfo = Price.query.filter_by(optionid= int(item)).first()
                #         count = count + medinfo.price * 
                price.price = count

                db.session.add(price)
                db.session.commit()
                flash('处方已经上传完成')
                return redirect(url_for('outpatient.opindex', name= name))

@outpatient.route('/outpatient/cost', methods= ['GET', 'POST'])
@is_login
def cost(name):
        cost = OpCost()
        nowpcheckid = int(request.cookies.get('nopcid'))
        if request.method == 'GET':
                opcheckininfo = OpCheckinAfford.query.filter_by(opcheckinid= nowpcheckid).first()
                opexaminfo = OpExamAfford.query.filter_by(opcheckinid= nowpcheckid).first()
                opcheckinfo = OpCheckAfford.query.filter_by(opcheckinid= nowpcheckid).first()
                oprecipeinfo = OpRecipeAfford.query.filter_by(opcheckinid= nowpcheckid).first()
                ociprice = opcheckininfo.price
                oeprice = opexaminfo.price
                ocprice = opcheckinfo.price
                orprice = oprecipeinfo.price

                cost.opcheckinid = nowpcheckid
                cost.price = ociprice + oeprice + ocprice + orprice

                price = cost.price
                
                db.session.add(cost)
                db.session.commit()
                return render_template('outpatient/cost.html', price= price, name= name)