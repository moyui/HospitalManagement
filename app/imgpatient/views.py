from flask import render_template, redirect, request, url_for, flash, make_response
from flask_session import Session
from .import imgpatient
from .form import ImgpCheckinForm, ImgpRecipeForm
from ..model import  Medicine, Price, UserInfo, ImgDoctorTimetable, ImgpCheckin, ImgpCheckinAfford, ImgpRecipe, ImgpRecipeAfford, ImgpCost
from ..decorator import is_login
from .. import db
import datetime

@imgpatient.route('/imgpatient/checkin', methods= ['GET', 'POST'])
@is_login
def checkin(name):
        patientcheckin = ImgpCheckin()
        form = ImgpCheckinForm()
        price = ImgpCheckinAfford()
        if request.method == 'GET':
                return render_template('imgpatient/checkin.html', form= form, name= name)
        else:
                if form.validate_on_submit():
                        response = make_response(redirect(url_for('imgpatient.imgpindex')))
                        prepatient = ImgpCheckin.query.order_by(ImgpCheckin.imgpcheckinid.desc()).first()
                        patientcheckin.imgpcheckinid = prepatient.imgpcheckinid + 1

                        nowpcheckid = patientcheckin.imgpcheckinid
                        response.set_cookie('nopcid', str(nowpcheckid))

                        patientcheckin.patientid = form.patientid.data
                        patientcheckin.doctorid = form.doctorname.data
                        docid = UserInfo.query.filter_by(id= form.doctorname.data).first()
                        patientcheckin.doctortype = docid.rank

                        price.imgpcheckinid = patientcheckin.imgpcheckinid
                        price.imgpid = form.patientid.data
                        priceinfo = Price.query.filter_by(optionid= docid.rank).first()
                        price.price = priceinfo.price

                        db.session.add(patientcheckin)
                        db.session.add(price)
                        db.session.commit()

                        return response

@imgpatient.route('/imgpatient/imgpindex', methods= ['GET', 'POST'])
@is_login
def imgpindex(name):
        nowpcheckid = int(request.cookies.get('nopcid'))
        if request.method == 'GET':
                # nowpcheckid = request.cookies.get('nopcid')
                # print('2', type(int(nowpcheckid)), int(nowpcheckid))
                return render_template('imgpatient/imgpindex.html', name= name)
    
@imgpatient.route('/imgpatient/recipe', methods= ['GET', 'POST'])
@is_login
def recipe(name):
        patientrecipe=ImgpRecipe()
        form = ImgpRecipeForm()
        nowpcheckid = request.cookies.get('nopcid')
        if request.method == 'GET':
               return render_template('/imgpatient/medicine.html', form= form, name= name)
        else: 
                if form.validate_on_submit():
                        patientrecipe.imgpcheckinid = int(nowpcheckid)
                        patientrecipe.imgpid = form.imgpid.data
                        patientrecipe.medicinenames = ','.join(form.medicines.data)
                        db.session.add(patientrecipe)
                        db.session.commit()
                        return redirect(url_for('imgpatient.recipenum', name= name))

@imgpatient.route('/imgpatient/recipenum', methods= ['GET', 'POST'])
@is_login
def recipenum(name):
        nowpcheckid = request.cookies.get('nopcid')
        price = ImgpRecipeAfford()
        if request.method == 'GET':
                patientcheckinid = int(nowpcheckid)
                selectedinfo = ImgpRecipe.query.filter_by(imgpcheckinid= patientcheckinid).first()
                medicinenames = selectedinfo.medicinenames
                medslist = medicinenames.split(',')
                medsnlist = []
                for item in medslist:
                        med = Medicine.query.filter_by(id= item).first()
                        medname = med.medicinename
                        medsnlist.append(medname)
                return render_template('imgpatient/recipenum.html', medsnlist= medsnlist, name= name)
        else:
                patientcheckinid = int(nowpcheckid)
                imgprecipe = ImgpRecipe.query.filter(ImgpRecipe.imgpcheckinid == patientcheckinid).first()
                mednumbers = []
                d = request.values.to_dict()
                for number in d.keys():
                        mednumbers.append(d.get(number))
                imgprecipe.medicinenumbers = ','.join(mednumbers)
                db.session.commit()

                price.imgpcheckinid = patientcheckinid
                imgpreinfo = ImgpRecipe.query.filter_by(imgpcheckinid= patientcheckinid).first()
                price.imgpid = imgpreinfo.imgpid
                recipeinfo = ImgpRecipe.query.filter_by(imgpcheckinid= patientcheckinid).first()
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
                return redirect(url_for('imgpatient.imgpindex', name= name))

@imgpatient.route('/imgpatient/cost', methods= ['GET', 'POST'])
@is_login
def cost(name):
        cost = ImgpCost()
        nowpcheckid = int(request.cookies.get('nopcid'))
        if request.method == 'GET':
                imgpcheckininfo = ImgpCheckinAfford.query.filter_by(imgpcheckinid= nowpcheckid).first()
                imgprecipeinfo = ImgpRecipeAfford.query.filter_by(imgpcheckinid= nowpcheckid).first()
                ociprice = imgpcheckininfo.price
                orprice = imgprecipeinfo.price

                cost.imgpcheckinid = nowpcheckid
                cost.price = ociprice + orprice

                price = cost.price
                
                db.session.add(cost)
                db.session.commit()
                return render_template('imgpatient/cost.html', price= price, name= name)