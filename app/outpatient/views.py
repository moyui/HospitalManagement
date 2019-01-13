from flask import render_template, redirect, request, url_for, flash, make_response
from . import outpatient
from .form import OpCheckForm, OpCheckinForm, OpCheckinTwoForm, OpExamForm, OpRecipeForm, OpIndexForm, OpSearchForm, OpCostListForm, OpExitForm
from ..model import OpCheck, OpCheckAfford, OpCheckin, OpCheckinAfford, OpExam, OpExamAfford, OpRecipe, OpRecipeAfford, Medicine, Price, UserInfo, OpCost, PatientInfo, DoctorTimetable, ExpertsTimetable, HospitalClass, ExamItem, CheckItem
from .. import db
from ..decorator import is_login, isauth
from datetime import datetime


@outpatient.route('/outpatient/checkin', methods=['GET', 'POST'])
@is_login
@isauth
def checkin(name, auth):
        form = OpCheckinForm()

        d = request.values.to_dict()
        for key in d.keys():
            temp = d.get(key)
        patientid = temp

        dt = datetime.now()
        dw = dt.weekday()

        dn = []
        drank = ''

        if request.method == 'GET':
            dtimetable = DoctorTimetable.query.filter_by(doctortime= dw).all()
            etimetable = ExpertsTimetable.query.filter_by(date= dw).all()

            for i in dtimetable:
                dinfo = UserInfo.query.filter_by(id= i.doctorid).first()
                dname = dinfo.name
                if dinfo.rank == 0:
                    drank = '普通医生'
                if dinfo.rank == 1:
                    drank = '副主任医生'
                if dinfo.rank == 2:
                    drank = '主治医师'
                dclass = HospitalClass.query.filter_by(id= i.cid).first()
                dstatus = drank + ':' + dname + '-----' + dclass.name
                dn.append(dstatus)
            
            for i in etimetable:
                einfo = UserInfo.query.filter_by(id= i.userinfoid).first()
                ename = einfo.name
                eclass = HospitalClass.query.filter_by(id= i.cid).first()
                estatus = '专家：' + ename + '-----' + eclass.name
                dn.append(estatus)

            return render_template('outpatient/checkin.html', form= form, name= name, auth= auth, dn= dn)

        else:
            doctorid = form.doctorname.data
            docid = UserInfo.query.filter_by(id= form.doctorname.data).first()
            doctortype = docid.rank

            response = make_response(redirect(url_for('outpatient.checkintwo')))
            prepatient = OpCheckin.query.order_by(OpCheckin.opcheckinid.desc()).first()
            checkinid = prepatient.opcheckinid + 1
            response.set_cookie('nopcid', str(checkinid))
            response.set_cookie('pid', patientid)
            response.set_cookie('did', doctorid)
            response.set_cookie('dt', str(doctortype))
            
            return response
            # return render_template('outpatient/checkintwo.html', patientid= patientid, doctorid= doctorid, doctortype= doctortype, name= name, auth= auth)
                # if form.validate_on_submit():
                #     response = make_response(redirect(url_for('main.index', name= name)))
                #     prepatient = OpCheckin.query.order_by(OpCheckin.opcheckinid.desc()).first()
                #     patientcheckin.opcheckinid = prepatient.opcheckinid + 1

                    # nowpcheckid = patientcheckin.opcheckinid
                    # response.set_cookie('nopcid', str(nowpcheckid))

                #     d = request.values.to_dict()
                #     for key in d.keys():
                #         temp = d.get(key)
                #     patientcheckin.patientid = temp
                #     patientcheckin.doctorid = form.doctorname.data
                #     docid = UserInfo.query.filter_by(id= form.doctorname.data).first()
                #     patientcheckin.doctortype = docid.rank
                #     patientcheckin.jips = False
                #     db.session.add(patientcheckin)
                #     db.session.commit()

                #     price.opcheckinid = patientcheckin.opcheckinid
                #     price.opid = temp
                #     priceinfo = Price.query.filter_by(optionid= docid.rank).first()
                #     price.price = priceinfo.price


                #     db.session.add(price)
                #     db.session.commit()

                #     return response

@outpatient.route('/outpatient/checkintwo', methods= ['GET', 'POST'])
@is_login
@isauth
def checkintwo(name, auth):
    form = OpCheckinTwoForm()
    patientcheckin = OpCheckin()
    price = OpCheckinAfford()
    nowpcheckid = int(request.cookies.get('nopcid'))
    patientid = request.cookies.get('pid')
    doctorid = request.cookies.get('did')
    doctortype = int(request.cookies.get('dt'))

    if request.method == 'GET' :
        patientinfo = PatientInfo.query.filter_by(id= patientid).first()
        pname = patientinfo.name
        doctorinfo = UserInfo.query.filter_by(id= doctorid).first()
        dinfo = DoctorTimetable.query.filter_by(doctorid= doctorid).first()
        einfo = ExpertsTimetable.query.filter_by(userinfoid= doctorid).first()
        classn = ''
        if dinfo:
            dclass = HospitalClass.query.filter_by(cid= dinfo.cid).first()
            classn = dclass.name
        if einfo:
            eclass = HospitalClass.query.filter_by(cid= einfo.cid).first()
            classn = eclass.name
        dname = doctorinfo.name
        drank = ''
        if doctortype == 0:
            drank += '-----普通医生'
        elif doctortype == 1:
            drank += '-----副主治医师'
        elif doctortype == 2:
            drank += '-----主治医师'
        elif doctortype == 3:
            drank += '-----专家'
        pstr = '身份编号：' + patientid + ':' + pname
        dstr = '身份编号：' + doctorid + ':' + dname
        return render_template('outpatient/checkintwo.html', nowpcheckid= nowpcheckid, pstr= pstr, dstr= dstr, drank= drank, classn= classn, name= name, auth= auth, form= form)
    else :
        patientcheckin.opcheckinid = nowpcheckid
        patientcheckin.patientid = patientid
        patientcheckin.doctorid = doctorid
        patientcheckin.doctortype = doctortype
        patientcheckin.jips = False
        db.session.add(patientcheckin)
        db.session.commit()

        price.opcheckinid = patientcheckin.opcheckinid
        price.opid = patientid
        priceinfo = Price.query.filter_by(optionid= doctortype).first()
        price.price = priceinfo.price


        db.session.add(price)
        db.session.commit()

        return render_template('/welcome.html', name=name, auth= auth)

@outpatient.route('/outpatient/opindex', methods= ['GET', 'POST'])
@is_login
@isauth
def opindex(name, auth):
    form = OpIndexForm()
    # nowpcheckid = int(request.cookies.get('nopcid'))
    if request.method == 'GET' :
        if request.cookies.get('nopcid'):
            return render_template('outpatient/opindex.html', form=form, name=name, auth= auth)
        else :
            flash('请先挂号')
            return redirect(url_for('main.index'))
    else:
        nowpcheckid = int(request.cookies.get('nopcid'))
        if form.inpatientcheck.data == True:
            opcheckininfo = OpCheckin.query.filter_by(
                opcheckinid=nowpcheckid).first()
            opcheckininfo.jips = True
            db.session.commit()
            flash('已登记住院，请前往住院系统办理相关手续')
        else:
            pass
        return render_template('outpatient/opindex.html', form=form, name=name, auth= auth)

@outpatient.route('/outpatient/show', methods= ['GET', 'POST'])
@is_login
@isauth
def opshow(name, auth):
    dt = datetime.now()
    dw = dt.weekday()
    nowpcheckid = int(request.cookies.get('nopcid'))
    ipstatus = '非住院患者'
    classname = ''
    drank = ''
    if request.method == 'GET' :
        checkininfo = OpCheckin.query.filter_by(opcheckinid= nowpcheckid).first()
        patientinfo = PatientInfo.query.filter_by(id= checkininfo.patientid).first()
        pname = patientinfo.name
        doctorinfo = UserInfo.query.filter_by(id= checkininfo.doctorid).first()
        dname = doctorinfo.name
        if doctorinfo.rank == 0 :
            drank = '普通医生'
        if doctorinfo.rank == 1 :
            drank = '副主治医师'
        if doctorinfo.rank == 2 :
            drank = '主治医师'
        if doctorinfo.rank == 3 :
            drank = '专家'
        dtime = DoctorTimetable.query.filter_by(doctorid= checkininfo.doctorid, doctortime= dw).first()
        etime = ExpertsTimetable.query.filter_by(userinfoid= checkininfo.doctorid, date= dw).first()
        if dtime:
            classinfo = HospitalClass.query.filter_by(id= dtime.cid).first()
            classname = classinfo.name
        if etime:
            classinfo = HospitalClass.query.filter_by(id= etime.cid).first()
            classname = classinfo.name
        if checkininfo.jips:
            ipstatus = '住院患者'
        return render_template('outpatient/show.html', nowpcheckid= nowpcheckid, pname= pname, dname= dname, drank= drank, classname= classname, ipstatus= ipstatus, name= name, auth= auth)

@outpatient.route('/outpatient/search', methods= ['GET', 'POST'])
@is_login
@isauth
def opsearch(name, auth):
    form = OpSearchForm()
    dt = datetime.now()
    dw = dt.weekday()
    ipstatus = '非住院患者'
    classname = ''
    if request.method == 'GET' :
        return render_template('outpatient/search.html', form= form, name= name, auth= auth)
    else :
        nowpcheckid = int(form.opcheckinid.data)
        checkininfo = OpCheckin.query.filter_by(opcheckinid= nowpcheckid).first()
        if checkininfo:
            patientinfo = PatientInfo.query.filter_by(id= checkininfo.patientid).first()
            pname = patientinfo.name
            doctorinfo = UserInfo.query.filter_by(id= checkininfo.doctorid).first()
            dname = doctorinfo.name
            if doctorinfo.rank == 0 :
                drank = '普通医生'
            if doctorinfo.rank == 1 :
                drank = '副主治医师'
            if doctorinfo.rank == 2 :
                drank = '主治医师'
            if doctorinfo.rank == 3 :
                drank = '专家'
            dtime = DoctorTimetable.query.filter_by(doctorid= checkininfo.doctorid, doctortime= dw).first()
            etime = ExpertsTimetable.query.filter_by(userinfoid= checkininfo.doctorid, date= dw).first()
            if dtime:
                classinfo = HospitalClass.query.filter_by(id= dtime.cid).first()
                classname = classinfo.name
            if etime:
                classinfo = HospitalClass.query.filter_by(id= etime.cid).first()
                classname = classinfo.name
            if checkininfo.jips:
                ipstatus = '住院患者'
            return render_template('outpatient/search.html', nowpcheckid= nowpcheckid, pname= pname, dname= dname, drank= drank, classname= classname, ipstatus= ipstatus, name= name, auth= auth, form= form)
        else :
            flash('暂无该挂号单号信息')
            return render_template('outpatient/search.html', form= form, name= name, auth= auth)

@outpatient.route('/outpatient/exam', methods=['GET', 'POST'])
@is_login
@isauth
def exam(name, auth):
    patientexam = OpExam()
    form = OpExamForm()
    price = OpExamAfford()
    nowpcheckid = int(request.cookies.get('nopcid'))
    if request.method == 'GET':
        return render_template('outpatient/exam.html', form=form, name=name, auth= auth)
    else:
        if form.validate_on_submit():
            patientexam.opcheckinid = nowpcheckid
            checkininfo = OpCheckin.query.filter_by(opcheckinid= nowpcheckid).first()
            patientexam.opid = checkininfo.patientid
            patientexam.examitems = ','.join(form.examitems.data)

            price.opcheckinid = patientexam.opcheckinid
            price.opid = patientexam.opid
            count = 0
            for item in form.examitems.data:
                examinfo = Price.query.filter_by(optionid=int(item)).first()
                count = count + examinfo.price
            price.price = count

            db.session.add(patientexam)
            db.session.add(price)
            db.session.commit()
            flash('选择的检验项目已经上传')
            return redirect(url_for('outpatient.opindex', name= name, auth= auth))

@outpatient.route('/outpatient/check', methods=['GET', 'POST'])
@is_login
@isauth
def check(name, auth):
    patientcheck = OpCheck()
    form = OpCheckForm()
    price = OpCheckAfford()
    nowpcheckid = int(request.cookies.get('nopcid'))
    if request.method == 'GET':
        return render_template('outpatient/check.html', form=form, name=name, auth= auth)
    else:
        if form.validate_on_submit():
            patientcheck.opcheckinid = nowpcheckid
            checkininfo = OpCheckin.query.filter_by(opcheckinid= nowpcheckid).first()
            patientcheck.opid = checkininfo.patientid
            patientcheck.checkitems = ','.join(form.checkitems.data)

            price.opcheckinid = patientcheck.opcheckinid
            price.opid = patientcheck.opid
            count = 0
            for item in form.checkitems.data:
                checkinfo = Price.query.filter_by(optionid=int(item)).first()
                count = count + checkinfo.price
            price.price = count

            db.session.add(patientcheck)
            db.session.add(price)
            db.session.commit()
            flash('选择的检查项目已经上传')
            return redirect(url_for('outpatient.opindex', name=name, auth= auth))


@outpatient.route('/outpatient/recipe', methods=['GET', 'POST'])
@is_login
@isauth
def recipe(name, auth):
    patientrecipe = OpRecipe()
    form = OpRecipeForm()
    nowpcheckid = int(request.cookies.get('nopcid'))
    if request.method == 'GET':
        return render_template('/outpatient/medicine.html', form=form, name=name, auth= auth)
    else:
        if form.validate_on_submit():
            patientrecipe.opcheckinid = nowpcheckid
            checkininfo = OpCheckin.query.filter_by(opcheckinid= nowpcheckid).first()
            patientrecipe.opid = checkininfo.patientid
            patientrecipe.medicinenames = ','.join(form.medicines.data)
            db.session.add(patientrecipe)
            db.session.commit()
            return redirect(url_for('outpatient.recipenum', name=name, auth= auth))


@outpatient.route('/outpatient/recipenum', methods=['GET', 'POST'])
@is_login
@isauth
def recipenum(name, auth):
    nowpcheckid = request.cookies.get('nopcid')
    price = OpRecipeAfford()
    if request.method == 'GET':
        patientcheckinid = int(nowpcheckid)
        selectedinfo = OpRecipe.query.filter_by(
            opcheckinid=patientcheckinid).first()
        medicinenames = selectedinfo.medicinenames
        medslist = medicinenames.split(',')
        medsnlist = []
        for item in medslist:
            med = Medicine.query.filter_by(id=item).first()
            medname = med.medicinename
            medsnlist.append(medname)
        return render_template('outpatient/recipenum.html', medsnlist=medsnlist, name=name, auth= auth)
    else:
        patientcheckinid = int(nowpcheckid)
        oprecipe = OpRecipe.query.filter(
            OpRecipe.opcheckinid == patientcheckinid).first()
        mednumbers = []
        d = request.values.to_dict()
        for number in d.keys():
            mednumbers.append(d.get(number))
        mednumbers.pop(-1)
        mednumbers.pop(-1)
        oprecipe.medicinenumbers = ','.join(mednumbers)
        db.session.commit()

        price.opcheckinid = patientcheckinid
        opreinfo = OpRecipe.query.filter_by(
            opcheckinid=patientcheckinid).first()
        price.opid = opreinfo.opid
        recipeinfo = OpRecipe.query.filter_by(
            opcheckinid=patientcheckinid).first()
        recipemdname = recipeinfo.medicinenames
        recipemdnamel = recipemdname.split(',')
        recipenum = recipeinfo.medicinenumbers
        recipenuml = recipenum.split(',')
        count = 0
        zipinfo = zip(recipemdnamel, recipenuml)
        for item in zipinfo:
            medinfo = Price.query.filter_by(optionid=int(item[0])).first()
            count = count + medinfo.price * int(item[1])
        # for item in recipemdnamel:
        #         medinfo = Price.query.filter_by(optionid= int(item)).first()
        #         count = count + medinfo.price *
        price.price = count

        db.session.add(price)
        db.session.commit()
        flash('处方已经上传完成')
        return redirect(url_for('outpatient.opindex'))

@outpatient.route('/outpatient/costlist', methods= ['GET', 'POST'])
@is_login
@isauth
def costlist(name, auth):
    form = OpCostListForm()
    nowpcheckid = int(request.cookies.get('nopcid'))
    ename = []
    cname = []
    mname = []
    m = {}
    examcost = 0
    checkcost = 0
    recipecost =0
    if request.method == 'GET' :
        return render_template('/outpatient/costlist.html', form= form, name= name, auth= auth, nowpcheckid= nowpcheckid, m= m)
    else :
        checkinid = int(form.opcheckinid.data)
        exams = OpExam.query.filter_by(opcheckinid= checkinid).first()
        if exams:
            examitems = exams.examitems.split(',')
            for item in examitems :
                exam = ExamItem.query.filter_by(id= item).first()
                ename.append(exam.examitemname)
        checks = OpCheck.query.filter_by(opcheckinid= checkinid).first()
        if checks:
            checkitems = checks.checkitems.split(',')
            for item in checkitems :
                check = CheckItem.query.filter_by(id= item).first()
                cname.append(check.checkitemname)
        medicines = OpRecipe.query.filter_by(opcheckinid= checkinid).first()
        if medicines :
            medicineslist = medicines.medicinenames.split(',')
            for item in medicineslist :
                iteminfo = Medicine.query.filter_by(id= item).first()
                mname.append(iteminfo.medicinename)
            medicinesnumberlist = medicines.medicinenumbers.split(',')
            m = dict(zip(mname, medicinesnumberlist))
        checkin = OpCheckinAfford.query.filter_by(opcheckinid= checkinid).first()
        if checkin:
            checkincost = checkin.price
            pexam = OpExamAfford.query.filter_by(opcheckinid= checkinid).first()
            if pexam:
                examcost = pexam.price
            pcheck = OpCheckAfford.query.filter_by(opcheckinid= checkinid).first()
            if pcheck:
                checkcost = pcheck.price
            precipe = OpRecipeAfford.query.filter_by(opcheckinid= checkinid).first()
            if precipe:
                recipecost = precipe.price
        else :
            flash('暂无该单号的费用记录')
        return render_template('outpatient/costlist.html', form= form, nowpcheckid= nowpcheckid, checkinid= checkinid, ename= ename, cname= cname, m= m, checkincost= checkincost, examcost= examcost, checkcost= checkcost, recipecost=recipecost, name= name, auth= auth)


@outpatient.route('/outpatient/cost', methods=['GET', 'POST'])
@is_login
@isauth
def cost(name, auth):
    cost = OpCost()
    nowpcheckid = int(request.cookies.get('nopcid'))
    ociprice = 0
    oeprice = 0
    ocprice = 0
    orprice = 0
    if request.method == 'GET':
        opcheckininfo = OpCheckinAfford.query.filter_by(
            opcheckinid=nowpcheckid).first()
        opexaminfo = OpExamAfford.query.filter_by(
            opcheckinid=nowpcheckid).first()
        opcheckinfo = OpCheckAfford.query.filter_by(
            opcheckinid=nowpcheckid).first()
        oprecipeinfo = OpRecipeAfford.query.filter_by(
            opcheckinid=nowpcheckid).first()
        if opcheckininfo:
            ociprice = opcheckininfo.price
        if opexaminfo:         
            oeprice = opexaminfo.price
        if opcheckinfo:
            ocprice = opcheckinfo.price
        if oprecipeinfo:
            orprice = oprecipeinfo.price

        cost.opcheckinid = nowpcheckid
        cost.cost = ociprice + oeprice + ocprice + orprice
 
        price = cost.cost

        db.session.add(cost)
        db.session.commit()
        return render_template('outpatient/cost.html', price= price, name= name, auth= auth)

@outpatient.route('/outpatient/exit', methods= ['GET', 'POST'])
@is_login
@isauth
def exit(name, auth):
    form = OpExitForm()
    if request.method == 'GET' :
        return render_template('outpatient/exit.html', form= form, name= name, auth= auth)
    else :
        response = make_response(redirect(url_for('main.index')))
        response.delete_cookie('nopcid')
        return response