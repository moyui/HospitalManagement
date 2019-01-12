from flask import render_template, redirect, request, url_for, flash
from . import familydoctor
from .form import FamilyPatientInfoForm, TestResultForm, SCListForm, FDCreateForm, FDAreaForm, FDLectureForm, FDdelete, FamilyDoctorShow, FamilyDoctorWorkShow, FamilyDoctorLecturekShow, FamilyDoctorpinfoshow
from ..model import FamilyDoctorArea, FamilyDoctor, FamilyDoctorWorkArea, FamilyPatientInfo, FamilyPatientTestResult, SpecialConcern, LecturePlace, LectureTime, UserInfo, DoctorTimetable
from .. import db
import datetime

@familydoctor.route('/familydoctor', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('/familydoctor/list.html')

@familydoctor.route('/familydoctor/PatientInfo', methods=['GET', 'POST'])
def fdpatientinfo():
    form = FamilyPatientInfoForm()
    pid = form.patientid.data
    if request.method == 'GET':
        return render_template('/familydoctor/patientinfo.html', form=form)
    else:
        if form.validate_on_submit():
            searchinfo = FamilyPatientInfo.query.filter_by(id = pid).first()
            if searchinfo:
                return render_template('/familydoctor/patientinfo.html', form=form, nodata=True)
            else:
                p = FamilyPatientInfo(
                id=form.patientid.data,
                FPname=form.name.data,
                FPage=form.age.data,
                FPsex=form.sex.data,
                FPphone=form.phone.data)
                db.session.add(p)
                db.session.commit()
                return redirect(url_for('familydoctor.fdpatientinfo'))

@familydoctor.route('/familydoctor/Testresult', methods=['GET', 'POST'])
def testresult():
    form = TestResultForm()
    pid = form.patientid.data
    if request.method == 'GET':
        return render_template('/familydoctor/Testresult.html', form=form)
    else:        
        if form.validate_on_submit():
            searchinfo = FamilyPatientInfo.query.filter_by(id = pid).first()
            if searchinfo:
                ts = FamilyPatientTestResult(
                    id = form.patientid.data + form.resultdate.data,
                    FPid = form.patientid.data,
                    FPname = form.name.data,
                    FPheartrate = form.fpheartrate.data,
                    FPbloodpressure = form.fpbloodpressure.data,
                    FPresultdate = form.resultdate.data
                    )
                db.session.add(ts)
                db.session.commit()
                return redirect(url_for('familydoctor.testresult'))
            else:
                return render_template('/familydoctor/Testresult.html', form=form, nodata=True)

@familydoctor.route('/familydoctor/SpecialConcern', methods=['GET', 'POST'])
def specialconcern():
    form = SCListForm()
    tdate = form.listdate.data
    if request.method == 'GET':
        return render_template('/familydoctor/specialconcern.html', form=form)
    else:        
        if form.validate_on_submit():
            searchinfo = FamilyPatientTestResult.query.filter_by(FPresultdate = tdate).all()
            if searchinfo:
                for item in searchinfo:
                    if (int(item.FPheartrate) > 100 or int(item.FPheartrate) < 80 or int(item.FPbloodpressure) > 140 or int(item.FPbloodpressure) < 110):
                        tfpid = item.FPid
                        searchinfo2 = SpecialConcern.query.filter_by(SCpid = tfpid).first()
                        if searchinfo2:
                            pass                        
                        else:
                            sc = SpecialConcern(
                                id = item.id,
                                SCpid = item.FPid,
                                SCpname = item.FPname,
                                SCpdate = item.FPresultdate,
                            )
                            db.session.add(sc)
                            db.session.commit()
            return redirect(url_for('familydoctor.specialconcern'))

@familydoctor.route('/familydoctor/areainfo', methods=['GET', 'POST'])
def areainfo():
    form = FDAreaForm()
    if request.method == 'GET':
        return render_template('/familydoctor/area.html', form=form)
    else:
        if form.validate_on_submit():
            aid = form.areaid.data
            aname = form.areaname.data
            searchinfo = FamilyDoctorArea.query.filter_by(id = aid).first()
            if searchinfo:
                return render_template('/familydoctor/area.html', form=form, nodata = True)
            else:
                a = FamilyDoctorArea(
                    id = aid,
                    Areaname = aname,
                )
                db.session.add(a)
                db.session.commit()
                return redirect(url_for('familydoctor.areainfo'))

@familydoctor.route('/familydoctor/lectureinfo', methods=['GET', 'POST'])
def lectureinfo():
    form = FDLectureForm()
    if request.method == 'GET':
        return render_template('/familydoctor/lectureinfo.html', form=form)
    else:
        if form.validate_on_submit():
            lpid = form.lecid.data
            lpname = form.lecname.data
            searchinfo = LecturePlace.query.filter_by(id = lpid).first()
            if searchinfo:
                return render_template('/familydoctor/lectureinfo.html', form=form, nodata = True)
            else:
                a = LecturePlace(
                    id = lpid,
                    LPname = lpname,
                )
                db.session.add(a)
                db.session.commit()
                return redirect(url_for('familydoctor.lectureinfo'))

@familydoctor.route('/familydoctor/familydoctorcreate', methods=['GET', 'POST'])
def fdcreate():
    form = FDCreateForm()
    if request.method == 'GET':
        return render_template('/familydoctor/createfd.html', form=form)
    else:
        if form.validate_on_submit():
            searchinfo = UserInfo.query.filter_by(rank = 2).all()
            if searchinfo:
                for item in searchinfo:
                    fdid = item.id
                    fdname = item.name
                    list1 = [0,0,0,0,0,0,0]
                    i = 0
                    date = 0
                    searchinfo2 = DoctorTimetable.query.filter_by(doctorid = fdid).all()
                    if searchinfo2:
                        for item in searchinfo2:
                            if item.doctortime == 0:
                                list1[0] = 1
                            if item.doctortime == 1:
                                list1[1] = 1
                            if item.doctortime == 2:
                                list1[2] = 1
                            if item.doctortime == 3:
                                list1[3] = 1
                            if item.doctortime == 4:
                                list1[4] = 1
                            if item.doctortime == 5:
                                list1[5] = 1
                            if item.doctortime == 6:
                                list1[6] = 1
                            else:
                                pass
                    else:
                        pass
                    while i<7 :
                        if list1[i] == 0:
                            date = i
                        else:
                            pass
                        i = i + 1
                    
                    if date != 0:
                        fdinfo = FamilyDoctor(
                            id = fdid + fdname,
                            FDdoctorid = fdid,
                            FDdoctorname = fdname,
                            FDdoctorrank = 2,
                            FDdate = date,
                        )
                    searchinfo3 = FamilyDoctor.query.filter_by(FDdoctorid = fdid).first()
                    if searchinfo3:
                        pass
                    else:
                        db.session.add(fdinfo)
                        db.session.commit()
                searchinfo4 = FamilyDoctorArea.query.order_by(FamilyDoctorArea.id).all()
                searchinfo5 = FamilyDoctor.query.order_by(FamilyDoctor.id).all()
                i = 0
                a = 0
                b = 0
                for item in searchinfo4:
                    a = a + 1
                for item in searchinfo5:
                    b = b + 1
                if b >= a:
                    for item in searchinfo4:
                        fdwid = item.id
                        fdwname = item.Areaname
                        for item in searchinfo5:
                            fdid = item.FDdoctorid
                            fdname = item.FDdoctorname
                            fdwa = FamilyDoctorWorkArea(
                                id = fdwname + fdname,
                                FDid = fdid,
                                FDareaid = fdwid,
                                FDareaname = fdwname,
                            )
                            searchinfo6 = FamilyDoctorWorkArea.query.filter_by(FDid = fdid).first()
                            searchinfo7 = FamilyDoctorWorkArea.query.filter_by(FDareaid = fdwid).first()
                            if searchinfo6:
                                pass
                            else:
                                if searchinfo7:
                                    pass
                                else:
                                    db.session.add(fdwa)
                                    db.session.commit()
                if a > b:
                    for item in searchinfo5:
                        fdid = item.FDdoctorid
                        fdname = item.FDdoctorname
                        for item in searchinfo4:
                            fdwid = item.id
                            fdwname = item.Areaname
                            fdwa = FamilyDoctorWorkArea(
                                id = fdwname + fdname,
                                FDid = fdid,
                                FDareaid = fdwid,
                                FDareaname = fdwname,
                            )
                            searchinfo6 = FamilyDoctorWorkArea.query.filter_by(FDid = fdid).first()
                            searchinfo7 = FamilyDoctorWorkArea.query.filter_by(FDareaid = fdwid).first()
                            if searchinfo6:
                                pass
                            else:
                                if searchinfo7:
                                    pass
                                else:
                                    db.session.add(fdwa)
                                    db.session.commit()
                searchinfo8 = LecturePlace.query.order_by(LecturePlace.id).all()
                searchinfo9 = FamilyDoctor.query.order_by(FamilyDoctor.id).all()
                i = 0
                a = 0
                b = 0
                for item in searchinfo8:
                    a = a + 1
                for item in searchinfo9:
                    b = b + 1
                if b >= a:
                    for item in searchinfo8:
                        lpid = item.id
                        lpname = item.LPname
                        for item in searchinfo9:
                            fdid = item.FDdoctorid
                            fddate = item.FDdate
                            lt = LectureTime(
                                id = fdid + lpname + fddate,
                                FDid = fdid,
                                LPid = lpid,
                                LPname = lpname,
                                LPdate = fddate,
                            )
                            searchinfo10 = LectureTime.query.filter_by(FDid = fdid).first()
                            searchinfo11 = LectureTime.query.filter_by(LPid = lpid).first()
                            if searchinfo10:
                                pass
                            else:
                                if searchinfo11:
                                    pass
                                else:
                                    db.session.add(lt)
                                    db.session.commit()
                if a > b:
                    for item in searchinfo9:
                        fdid = item.FDdoctorid
                        fddate = item.FDdate
                        for item in searchinfo8:
                            lpid = item.id
                            lpname = item.LPname
                            lt = LectureTime(
                                id = fdid + lpname + fddate,
                                FDid = fdid,
                                LPid = lpid,
                                LPname = lpname,
                                LPdate = fddate,
                            )
                            searchinfo10 = LectureTime.query.filter_by(FDid = fdid).first()
                            searchinfo11 = LectureTime.query.filter_by(LPid = lpid).first()
                            if searchinfo10:
                                pass
                            else:
                                if searchinfo11:
                                    pass
                                else:
                                    db.session.add(lt)
                                    db.session.commit()
                return redirect(url_for('familydoctor.fdcreate'))
            else:
                return redirect(url_for('familydoctor.fdcreate'))

@familydoctor.route('/familydoctor/familydoctordelete', methods=['GET', 'POST'])
def fddelete():
    form = FDdelete()
    if request.method == 'GET':
        return render_template('/familydoctor/deletefd.html', form=form)
    else:
        if form.validate_on_submit():
            searchinfo = FamilyDoctor.query.filter_by(FDdoctorid = form.fddid.data).first()
            if searchinfo:
                db.session.delete(searchinfo)
                db.session.commit()
            searchinfo2 = FamilyDoctorWorkArea.query.filter_by(FDid = form.fddid.data).first()
            if searchinfo2:
                db.session.delete(searchinfo2)
                db.session.commit()
            searchinfo3 = LectureTime.query.filter_by(FDid = form.fddid.data).first()
            if searchinfo3:
                db.session.delete(searchinfo3)
                db.session.commit()
            return redirect(url_for('familydoctor.fddelete'))

@familydoctor.route('/familydoctor/familydoctorshow', methods=['GET', 'POST'])
def familydoctorshow():
    form = FamilyDoctorShow()
    searchinfo = FamilyDoctor.query.order_by(FamilyDoctor.id).all()
    if request.method == 'GET':
        return render_template('/familydoctor/fdshow.html', form = form)
    else:
        if form.validate_on_submit():
            return render_template('/familydoctor/fdshow.html', form = form, fdinfo = searchinfo)

@familydoctor.route('/familydoctor/familydoctorworkshow', methods=['GET', 'POST'])
def familydoctorworkshow():
    form = FamilyDoctorWorkShow()
    searchinfo = FamilyDoctorWorkArea.query.order_by(FamilyDoctorWorkArea.id).all()
    if request.method == 'GET':
        return render_template('/familydoctor/fdwshow.html', form = form)
    else:
        if form.validate_on_submit():
            return render_template('/familydoctor/fdwshow.html', form = form, fdwinfo = searchinfo)

@familydoctor.route('/familydoctor/familydoctorlecturehow', methods=['GET', 'POST'])
def familydoctorlecturehow():
    form = FamilyDoctorLecturekShow()
    searchinfo = LectureTime.query.order_by(LectureTime.id).all()
    if request.method == 'GET':
        return render_template('/familydoctor/fdlshow.html', form = form)
    else:
        if form.validate_on_submit():
            return render_template('/familydoctor/fdlshow.html', form = form, fdlinfo = searchinfo)

@familydoctor.route('/familydoctor/familydoctorpinfoshow', methods=['GET', 'POST'])
def familyDoctorpinfoshow():
    form = FamilyDoctorpinfoshow()
    pid = form.patientid.data
    searchinfo = FamilyPatientInfo.query.filter_by(id = pid).all()
    if request.method == 'GET':
        return render_template('/familydoctor/fdpinfoshow.html', form = form)
    else:
        if form.validate_on_submit():
            return render_template('/familydoctor/fdpinfoshow.html', form = form, fdpinfo = searchinfo)

@familydoctor.route('/familydoctor/familydoctortrshow', methods=['GET', 'POST'])
def familyDoctorptsshow():
    form = FamilyDoctorpinfoshow()
    pid = form.patientid.data
    searchinfo = FamilyPatientTestResult.query.filter_by(FPid = pid).all()
    if request.method == 'GET':
        return render_template('/familydoctor/fdptrshow.html', form = form)
    else:
        if form.validate_on_submit():
            return render_template('/familydoctor/fdptrshow.html', form = form, fdptrinfo = searchinfo)

@familydoctor.route('/familydoctor/scshow', methods=['GET', 'POST'])
def scshow():
    form = FamilyDoctorLecturekShow()
    searchinfo = SpecialConcern.query.order_by(SpecialConcern.id).all()
    if request.method == 'GET':
        return render_template('/familydoctor/scshow.html', form = form)
    else:
        if form.validate_on_submit():
            return render_template('/familydoctor/scshow.html', form = form, scinfo = searchinfo)
