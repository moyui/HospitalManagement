from . import db
# 对应的关系表 比如1-男 0-女 0-普通 1-副主治 2-主治 3-专家等写死还是创建表


class UserGroup(db.Model):
    __tablename__ = 'usergroup'
    id = db.Column(db.Integer, primary_key=True)  # 每个用户记得添加用户组
    name = db.Column(db.String(64))


class UserInfo(db.Model):  # 医生，管理员，院长一张表
    __tablename__ = 'userinfo'
    id = db.Column(db.String(64), primary_key=True)  # 身份证号
    name = db.Column(db.String(64))
    sex = db.Column(db.Integer)
    rank = db.Column(db.Integer)  # 0-普通 1-副主治 2-主治 3-专家
    password = db.Column(db.String(64))
    groupid = db.Column(db.Integer, db.ForeignKey('usergroup.id'))


class HospitalConstuct(db.Model):
    __tablename__ = 'hospitalconstuct'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    hospitalclass = db.relationship(
        'HospitalClass', backref='itsclasss', lazy='dynamic')


class HospitalClass(db.Model):
    __tablename__ = 'hospitalclass'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # date = db.Column(db.String(128))
    cid = db.Column(db.Integer, db.ForeignKey('hospitalconstuct.id'))
    # 时间跟着医生走，需要一张类似于选课，医生与科室的视图（工作时间）。防止时间冲突


class PatientInfo(db.Model):
    __tablename__ = 'patientinfo'
    id = db.Column(db.String(64), primary_key=True)  # 身份证号
    name = db.Column(db.String(64))
    birth = db.Column(db.Date)
    sex = db.Column(db.Integer)  # 1-男 0-女
    age = db.Column(db.Integer)

# 医生轮作


class DoctorCycle(db.Model):
    __tablename__ = 'doctorcycle'
    id = db.Column(db.Integer, primary_key=True)
    doctorid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
    classid = db.Column(db.String(64), db.ForeignKey('hospitalclass.id'))


class OutPatientTimetable(db.Model):
    __tablename__ = 'outpatienttimetable'
    id = db.Column(db.Integer, primary_key=True)
    doctorcycleid = db.Column(db.Integer, db.ForeignKey('doctorcycle.id'))
    date = db.Column(db.String(128))  # 准备一个时间段与字符串数字相对应 01 -> 9:00 - 10： 00


class InPatientTimetable(db.Model):
    __tablename__ = 'inpatienttimetable'
    id = db.Column(db.Integer, primary_key=True)
    userinfoid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
    date = db.Column(db.String(128))

# 缺少急诊


class ExpertsTimetable(db.Model):
    __tablename__ = 'expertstimetable'
    id = db.Column(db.Integer, primary_key=True)
    userinfoid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
    cid = db.Column(db.String(64), db.ForeignKey('hospitalclass.id'))
    date = db.Column(db.String(128))


class Medicine(db.Model):
    __tablename__ = 'medicine'
    id = db.Column(db.Integer, primary_key=True)  # 6位，1开头，自增
    medicineclass = db.Column(db.Integer)  # 药品类别， 0代表中药， 1代表西药
    medicinename = db.Column(db.String(128))


class CheckClass(db.Model):
    __tablename__ = 'checkclass'
    id = db.Column(db.Integer, primary_key=True)
    checkcname = db.Column(db.String(64))


class CheckItem(db.Model):
    __tablename__ = 'checkitem'
    id = db.Column(db.String(128), primary_key=True)  # 6位，2开头，自增
    checkitemname = db.Column(db.String(64))
    itemclass = db.Column(db.Integer, db.ForeignKey('checkclass.id'))


class ExamClass(db.Model):
    __tablename__ = 'examclass'
    id = db.Column(db.Integer, primary_key=True)  # 6位，3开头，自增
    examname = db.Column(db.String(64))


class ExamItem(db.Model):
    __tablename__ = 'examitem'
    id = db.Column(db.String(128), primary_key=True)
    examitemname = db.Column(db.String(64))
    itemclass = db.Column(db.Integer, db.ForeignKey('checkclass.id'))


class InhospitalArea(db.Model):
    __tablename__ = 'inhospitalarea'
    id = db.Column(db.Integer, primary_key=True)
    areaname = db.Column(db.String(64))


class BedInfo(db.Model):
    __tablename__ = 'bedinfo'
    id = db.Column(db.Integer, primary_key=True)
    areaid = db.Column(db.Integer, db.ForeignKey('inhospitalarea.id'))


class Price(db.Model):
    __tablename__ = 'price'
    id = db.Column(db.String(20), primary_key=True)
    optionid = db.Column(db.Integer)  # 为药品、检查、检验ID
    price = db.Column(db.Float)

# from . import db

# class FamilyDoctorArea(db.Model):                    #家庭医生服务区域
#     __tablename__ = 'fdarea'
#     Areaid = db.Column(db.Integer, primary_key=True)
#     Areaname = db.Column(db.String(64))

# class FamilyDoctorTeam(db.Model):                    #创建家庭医生团队
#     __tablename__ = 'fdteam'
#     FDTid = db.Column(db.Integer, primary_key=True)
#     FDTareaid = db.Column(db.Integer, db.ForeignKey('fdarea.Areaid'))
#     FDTareaname = db.Column(db.String(64), db.ForeignKey('fdarea.Areaname'))
#     FDTdoctorid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
#     FDTdoctorname = db.Column(db.String(64), db.ForeignKey('userinfo.name'))
#     FDTdoctorrank = db.Column(db.Integer, db.ForeignKey('userinfo.rank'))
#     FDTteamdate = db.Column(db.String(128), db.ForeignKey('outpatienttimetable.date'))

# class FamilyPatientInfo(db.Model):                   #家庭医生病人基本信息
#     __tablename__ = 'fpinfo'
#     FPid1 = db.Column(db.String(64), primary_key=True)  #病人身份证号
#     FPname1 = db.Column(db.String(64))
#     FPage = db.Column(db.Integer)
#     FPsex = db.Column(db.String(64))
#     FPphone = db.Column(db.String(64))

# # class FamilyPatientTestResult(db.Model):             #体检结果
# #     __tablename__ = 'fptestresult'
# #     FPTRid = db.Column(db.Integer, primary_key=True)     #初始为1 自增
# #     FPid2 = db.Column(db.String(64), db.ForeignKey('fpinfo.FPid1'))
# #     FPname2 = db.Column(db.String(64), db.ForeignKey('fpinfo.FPname1'))
# #     FPheartrate = db.Column(db.Integer)       #心率
# #     FPbloodpressure = db.Column(db.Integer)   #血压

# # class SpecialConcern(db.Model):                      #特殊关注对象
# #     __tablename__ = 'specialconcern'
# #     SCid = db.Column(db.Integer, primary_key=True)     #初始为1 自增
# #     SCpid = db.Column(db.String(64), db.ForeignKey('fptestresult.FPid2'))      #特殊关注对象姓名
# #     SCpname = db.Column(db.String(64), db.ForeignKey('fptestresult.FPname2'))  #特殊关注对象身份证 传递给门诊部

# class LecturePlace(db.Model):
#     __tablename__ = 'lectureplace'
#     LPid = db.Column(db.Integer, primary_key=True)
#     LPname = db.Column(db.String(64))
#     LParea = db.Column(db.String(64))                  #安排讲座时area与团队领队医生的服务区域进行对比

# class LectureTime(db.Model):
#     __tablename__ = 'lecturename'
#     LTid = db.Column(db.Integer, primary_key=True)
#     LPid = db.Column(db.Integer, db.ForeignKey('lectureplace.LPid'))
#     LPname = db.Column(db.String(64))


class OpCheckin(db.Model):
    __tablename__ = 'opcheckin'
    id = db.Column(db.String(10), primary_key=True)
    patientid = db.Column(db.String(10), db.ForeignKey('patientinfo.id'))
    doctorid = db.Column(db.String(10), db.ForeignKey('userinfo.id'))
    doctime = db.Column(db.Integer, db.ForeignKey('outpatienttimetable.id'))
    experttime = db.Column(db.Integer, db.ForeignKey('expertstimetable.id'))
    # scsignal = db.Column(db.Integer) #与特别关注对象表对比，0为非关注，1为关注
    jips = db.Column(db.Boolean)


class OpExam(db.Model):
    __tablename__ = 'opexam'
    id = db.Column(db.String(10), db.ForeignKey(
        'opcheckin.id'), primary_key=True)
    examitems = db.Column(db.String(128), db.ForeignKey('examitem.id'))

class OpCheck(db.Model):
    __tablename__ = 'opcheck'
    id = db.Column(db.String(10), db.ForeignKey(
        'opcheckin.id'), primary_key=True)
    checkitems = db.Column(db.String(128), db.ForeignKey('checkitem.id'))


class OpRecipe(db.Model):
    __tablename__ = 'oprecipe'
    id = db.Column(db.String(10), db.ForeignKey(
        'opcheckin.id'), primary_key=True)
    medicinenames = db.Column(db.String(128))


class OpCheckinAfford(db.Model):
    __tablename__ = 'opcheckinafford'
    id = db.Column(db.String(10), db.ForeignKey(
        'opcheckin.id'), primary_key=True)
    price = db.Column(db.Float)


class OpExamAfford(db.Model):
    __tablename__ = 'opexamafford'
    id = db.Column(db.String(10), db.ForeignKey(
        'opcheckin.id'), primary_key=True)
    price = db.Column(db.Float)


class OpCheckAfford(db.Model):
    __tablename__ = 'opcheckafford'
    id = db.Column(db.String(10), db.ForeignKey(
        'opcheckin.id'), primary_key=True)
    price = db.Column(db.Float)


class OpRecipeAfford(db.Model):
    __tablename__ = 'oprecipeafford'
    id = db.Column(db.String(10), db.ForeignKey(
        'opcheckin.id'), primary_key=True)
    price = db.Column(db.Float)


class InPatientDeposit(db.Model):
    __tablename__ = 'inpatientdeposit'
    id = db.Column(db.Integer, primary_key=True)
    patientid = db.Column(db.String(10), db.ForeignKey('opcheckin.id'))
    rest = db.Column(db.Float)


class InPatientTotalCost(db.Model):
    __tablename__ = 'inpatienttotalcost'
    id = db.Column(db.Integer, db.ForeignKey(
        'inpatientdeposit.id'), primary_key=True)
    totalcost = db.Column(db.Float)
    unpaiditemsid = db.Column(db.String(64))  # 未支付项


class InPatientTableSet(db.Model):
    __tablename__ = 'inpatienttableset'
    id = db.Column(db.Integer, db.ForeignKey(
        'inpatientdeposit.id'), primary_key=True)
    inpatienttimeandbedid = db.Column(db.String(128))
    inpatientcheckid = db.Column(db.String(128))
    inpatientinspectid = db.Column(db.String(128))
    inpatientprescriptid = db.Column(db.String(128))
    close = db.Column(db.Boolean)


class InPatientTimeAndBed(db.Model):
    __tablename__ = 'inpatienttimeandbed'
    id = db.Column(db.String(64), primary_key=True)
    badid = db.Column(db.Integer, db.ForeignKey('bedinfo.id'))  # 待填写
    doctorinfoid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)


class InPatientCheck(db.Model):
    __tablename__ = 'inpatientcheck'
    id = db.Column(db.String(64), primary_key=True)
    checkitemsid = db.Column(db.String(128))
    doctorinfoid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))


class InPatientInspect(db.Model):
    __tablename__ = 'inpatientinspect'
    id = db.Column(db.String(64), primary_key=True)
    inspectitemsid = db.Column(db.String(128))
    doctorinfoid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))


class InPatientPrescript(db.Model):
    __tablename__ = 'inpatientprescript'
    id = db.Column(db.String(64), primary_key=True)
    prescriptitemsid = db.Column(db.String(128))
    doctorinfoid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
