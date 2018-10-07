from . import db

class HospitalConstuct(db.Model):
    __tablename__ = 'hospitalconstuct'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    hospitalclass = db.relativeship('HospitalClass', backref='itsclasss', lazy='dynamic')


class HospitalClass(db.Model):
    __tablename__ = 'hospitalclass'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # date = db.Column(db.String(128))
    cid = db.Column(db.Integer, db.ForeignKey('hospitalclass.id'))

    #时间跟着医生走，需要一张类似于选课，医生与科室的视图（工作时间）。防止时间冲突

class PatientInfo(db.Model):
    __tablename__ = 'patientinfo'
    id = db.Column(db.String(64), primary_key=True) #身份证号
    name = db.Column(db.String(64))
    birth = db.Column(db.Date)
    sex = db.Column(db.Integer) #1-男 0-女
    age = db.Column(db.Integer)

class DoctorInfo(db.Model):
    __tablename__ = 'doctorinfo'
    id = db.Column(db.String(64), primary_key=True) #身份证号
    name = db.Column(db.String(64))
    sex = db.Column(db.Integer)
    rank = db.Column(db.Integer) #0-普通 1-副主治 2-主治 3-专家

# 医生轮作
class DoctorCycle(db.Model):
    __tablename__ = 'doctorcycle'
    id = db.Column(db.Integer, primary_key=True)
    doctorid = db.Column(db.String(64), db.ForeignKey('doctorinfo.id'))
    classid = db.Column(db.String(64), db.ForeignKey('hospitalclass.id'))

class OutPatientTimetable(db.Model):
    __tablename__ = 'outpatienttimetable'
    id = db.Column(db.Integer, primary_key=True)
    doctorcycleid = db.Column(db.Integer, db.ForeignKey('doctorcycle.id'))
    date = db.Column(db.String(128)) #准备一个时间段与字符串数字相对应 01 -> 9:00 - 10： 00
    
class InPatientTimetable(db.Model):
    __tablename__ = 'inpatienttimetable'
    id = db.Column(db.Integer, primary_key=True)
    doctorinfoid = db.Column(db.String(64), db.ForeignKey('doctorinfo.id'))
    date = db.Column(db.String(128))

#缺少急诊

class ExpertsTimetable(db.Model):
    __tablename__ = 'expertstimetable'
    id = db.Column(db.Integer, primary_key=True)
    doctorinfoid = db.Column(db.String(64), db.ForeignKey('doctorinfo.id'))
    cid = db.Column(db.Integer, db.ForeignKey('hospitalclass.id'))
    date = db.Column(db.String(128))
