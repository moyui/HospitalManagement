from . import db

class FamilyDoctorArea(db.Model):                    #家庭医生服务区域
    __tablename__ = 'fdarea'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

class FamilyDoctorTeam(db.Model):                    #创建家庭医生团队
    __tablename__ = 'fdteam'
    id = db.Column(db.Integer, primary_key=True)
    teamareaid = db.Column(db.String(64), db.ForeignKey('fdarea.id'))
    teamareaname = db.Column(db.String(64), db.ForeignKey('fdarea.name'))
    doctorid = db.Column(db.String(64), db.ForeignKey('doctorinfo.id'))
    doctorname = db.Column(db.String(64), db.ForeignKey('doctorinfo.name'))
    doctorrank = db.Column(db.Integer, db.ForeignKey('doctorinfo.rank'))
    teamdate = db.Column(db.String(128), db.ForeignKey('outpatienttimetable.date'))

class FamilyPatientInfo(db.Model):                   #家庭医生病人基本信息
    __tablename__ = 'fpinfo'
    id = db.Column(db.String(64), primary_key=True)  #病人身份证号
    name = db.Column(db.String(64))
    age = db.Column(db.Integer)
    sex = db.Column(db.String(64))
    phone = db.Column(db.String(64))

class FamilyPatientTestResult(db.Model):             #体检结果
    __tablename__ = 'fptestresult'
    id = db.Column(db.Integer, primary_key=True)     #初始为1 自增
    fpid = db.Column(db.String(64), db.ForeignKey('fpinfo.id'))
    fpname = db.Column(db.String(64), db.ForeignKey('fpinfo.name'))
    heartrate = db.Column(db.Integer)       #心率
    bloodpressure = db.Column(db.Integer)   #血压

class SpecialConcern(db.Model):                      #特殊关注对象
    __tablename__ = 'specialconcern'
    id = db.Column(db.Integer, primary_key=True)     #初始为1 自增
    scid = db.Column(db.String(64), db.ForeignKey('fptestresult.fpid'))      #特殊关注对象姓名
    scname = db.Column(db.String(64), db.ForeignKey('fptestresult.fpname'))  #特殊关注对象身份证 传递给门诊部

class LecturePlace(db.Model):
    __tablename__ = 'lectureplace'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))                  
    area = db.Column(db.String(64))                  #安排讲座时area与团队领队医生的服务区域进行对比

class LectureTime(db.Model):
    __tablename__ = 'lecturename'
    id = db.Column(db.Integer, primary_key=True)
    lpid = db.Column(db.Integer, db.ForeignKey('lectureplace.id'))
    lpname = db.Column(db.String)