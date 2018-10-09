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
    cid = db.Column(db.Integer, db.FornignKey('hospitalclass.id'))

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
    doctorid = db.Column(db.String(64), db.FornignKey('doctorinfo.id'))
    classid = db.Column(db.String(64), db.FornignKey('hospitalclass.id'))

class OutPatientTimetable(db.Model):
    __tablename__ = 'outpatienttimetable'
    id = db.Column(db.Integer, primary_key=True)
    doctorcycleid = db.Column(db.Integer, db.FornignKey('doctorcycle.id'))
    date = db.Column(db.String(128)) #准备一个时间段与字符串数字相对应 01 -> 9:00 - 10： 00
    
class inPatientTimetable(db.Model):
    __tablename__ = 'inpatienttimetable'
    id = db.Column(db.Integer, primary_key=True)
    doctorinfoid = db.Column(db.String(64), db.FornignKey('doctorinfo.id'))
    date = db.Column(db.String(128))

#缺少急诊

class ExpertsTimetable(db.Model):
    __tablename__ = 'expertstimetable'
    id = db.Column(db.Integer, primary_key=True)
    doctorinfoid = db.Column(db.String(64), db.FornignKey('doctorinfo.id'))
    cid = db.Column(db.Integer, db.FornignKey('hospitalclass.id'))
    date = db.Column(db.String(128))

class Medicine(db.Model):
    __tablename__ = 'medicine'
    id = db.Column(db.Integer, primary_key=True) #6位，1开头，自增
    medicineclass = db.Column(db.Integer) #药品类别， 0代表中药， 1代表西药
    medicinename = db.Column(db.String(128))

class CheckClass(db.Model):
    __tablename__ = 'checkclass'
    id = db.Column(db.Integer, primary_key=True)
    checkcname = db.Column(db.String(64))

class CheckItem(db.Model):
    __tablename__ = 'checkitem'
    id = db.Column(db.Integer, primary_key=True) #6位，2开头，自增
    checkitemname = db.Column(db.String(64))
    itemclass = db.Column(db.Integer, db.FornignKey('checkclass.id'))

class ExamClass(db.Model):
    __tablename__ = 'examclass'
    id = db.Column(db.Integer, primary_key=True) #6位，3开头，自增
    examname = db.Column(db.String(64))

class ExamItem(db.Model):
    __tablename__ = 'examitem'
    id = db.Column(db.Integer, primary_key=True)
    examitemname = db.Column(db.String(64))
    itemclass = db.Column(db.Integer, db.FornignKey('checkclass.id'))

class InhospitalArea(db.Model):
    __tablename__ = 'inhospitalarea'
    id = db.Column(db.Integer, primary_key=True)
    areaname = db.Column(db.String(64))

class BedInfo(db.Model):
    __tablename__ = 'bedinfo'
    id = db.Column(db.Integer, primary_key=True)
    areaid = db.Column(db.Integer, db.FornignKey('inhospitalarea.id'))

class Price(db.Model):
    __tablename__ = 'price'
    optionid = db.Column(db.Integer) #为药品、检查、检验ID
    price = db.Column(db.Float)