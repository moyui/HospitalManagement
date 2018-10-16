from . import db

class FamilyDoctorArea(db.Model):                    #家庭医生服务区域
    __tablename__ = 'fdarea'
    Areaid = db.Column(db.Integer, primary_key=True)
    Areaname = db.Column(db.String(64))

class FamilyDoctorTeam(db.Model):                    #创建家庭医生团队
    __tablename__ = 'fdteam'
    FDTid = db.Column(db.Integer, primary_key=True)
    FDTareaid = db.Column(db.String(64), db.ForeignKey('fdarea.Areaid'))
    FDTareaname = db.Column(db.String(64), db.ForeignKey('fdarea.Areaname'))
    FDTdoctorid = db.Column(db.String(64), db.ForeignKey('doctorinfo.id'))
    FDTdoctorname = db.Column(db.String(64), db.ForeignKey('doctorinfo.name'))
    FDTdoctorrank = db.Column(db.Integer, db.ForeignKey('doctorinfo.rank'))
    FDTteamdate = db.Column(db.String(128), db.ForeignKey('outpatienttimetable.date'))

class FamilyPatientInfo(db.Model):                   #家庭医生病人基本信息
    __tablename__ = 'fpinfo'
    FPid = db.Column(db.String(64), primary_key=True)  #病人身份证号
    FPname = db.Column(db.String(64))
    FPage = db.Column(db.Integer)
    FPsex = db.Column(db.String(64))
    FPphone = db.Column(db.String(64))

class FamilyPatientTestResult(db.Model):             #体检结果
    __tablename__ = 'fptestresult'
    FPTRid = db.Column(db.Integer, primary_key=True)     #初始为1 自增
    FPid = db.Column(db.String(64), db.ForeignKey('fpinfo.FPid'))
    FPname = db.Column(db.String(64), db.ForeignKey('fpinfo.FPname'))
    FPheartrate = db.Column(db.Integer)       #心率
    FPbloodpressure = db.Column(db.Integer)   #血压

class SpecialConcern(db.Model):                      #特殊关注对象
    __tablename__ = 'specialconcern'
    SCid = db.Column(db.Integer, primary_key=True)     #初始为1 自增
    SCpid = db.Column(db.String(64), db.ForeignKey('fptestresult.FPid'))      #特殊关注对象姓名
    SCpname = db.Column(db.String(64), db.ForeignKey('fptestresult.FPname'))  #特殊关注对象身份证 传递给门诊部

class LecturePlace(db.Model):
    __tablename__ = 'lectureplace'
    LPid = db.Column(db.Integer, primary_key=True)
    LPname = db.Column(db.String(64))                  
    LParea = db.Column(db.String(64))                  #安排讲座时area与团队领队医生的服务区域进行对比

class LectureTime(db.Model):
    __tablename__ = 'lecturename'
    LTid = db.Column(db.Integer, primary_key=True)
    LPid = db.Column(db.Integer, db.ForeignKey('lectureplace.LPid'))
    LPname = db.Column(db.String)