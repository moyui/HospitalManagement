from . import db

class FamilyDoctorArea(db.Model):                    #家庭医生服务区域
    __tablename__ = 'fdarea'
    id = db.Column(db.Integer, primary_key=True)
    Areaname = db.Column(db.String(64))

class FamilyDoctorTeam(db.Model):                    #创建家庭医生团队
    __tablename__ = 'fdteam'
    id = db.Column(db.Integer, primary_key=True)
    FDTareaid = db.Column(db.Integer, db.ForeignKey('fdarea.id'))
    FDTareaname = db.Column(db.String(64))
    FDTdoctorid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
    FDTdoctorname = db.Column(db.String(64))
    FDTdoctorrank = db.Column(db.Integer)
    FDTteamdate = db.Column(db.String(128))

class FamilyPatientInfo(db.Model):                      #家庭医生病人基本信息
    __tablename__ = 'fpinfo'
    id = db.Column(db.String(64), primary_key=True)   #病人身份证号
    FPname = db.Column(db.String(64))
    FPage = db.Column(db.Integer)
    FPsex = db.Column(db.String(64))
    FPphone = db.Column(db.String(64))

class FamilyPatientTestResult(db.Model):             #体检结果
    __tablename__ = 'fptestresult'
    id = db.Column(db.Integer, primary_key=True)     #初始为1 自增
    FPid = db.Column(db.String(64), db.ForeignKey('fpinfo.id'))
    FPname = db.Column(db.String(64))
    FPheartrate = db.Column(db.Integer)       #心率
    FPbloodpressure = db.Column(db.Integer)   #血压

class SpecialConcern(db.Model):                      #特殊关注对象
    __tablename__ = 'specialconcern'
    id = db.Column(db.Integer, primary_key=True)                            #初始为1 自增
    SCpid = db.Column(db.String(64), db.ForeignKey('fptestresult.id'))
    SCpname = db.Column(db.String(64))                                      #特殊关注对象身份证 传递给门诊部

class LecturePlace(db.Model):
    __tablename__ = 'lectureplace'
    id = db.Column(db.Integer, primary_key=True)
    LPname = db.Column(db.String(64))                  
    LParea = db.Column(db.String(64))                                       #安排讲座时area与团队领队医生的服务区域进行对比

class LectureTime(db.Model):
    __tablename__ = 'lecturename'
    id = db.Column(db.Integer, primary_key=True)
    LPid = db.Column(db.Integer, db.ForeignKey('lectureplace.id'))
    LPname = db.Column(db.String(64))                  
    LPdate = db.Column(db.String(128))
