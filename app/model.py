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

<<<<<<< Updated upstream
=======
class DoctorTimetable(db.Model):
    __tablename__ = 'doctortimetable'
    id = db.Column(db.String(64), primary_key=True)
    doctorid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
    doctortime = db.Column(db.Integer)

# 医生轮作
>>>>>>> Stashed changes

class DoctorTimetable(db.Model):
    __tablename__ = 'doctortimetable'
    id = db.Column(db.String(64), primary_key=True)
    doctorid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
    doctortime = db.Column(db.Integer)

<<<<<<< Updated upstream
class ImgDoctorTimetable(db.Model):
    __tablename__ = 'imgdoctortimetable'
    id = db.Column(db.String(64), primary_key=True)
    doctorid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
    doctortime = db.Column(db.Integer)
=======
# class DoctorCycle(db.Model):
#     __tablename__ = 'doctorcycle'
#     id = db.Column(db.Integer, primary_key=True)
#     doctorid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
#     classid = db.Column(db.String(64), db.ForeignKey('hospitalclass.id'))
>>>>>>> Stashed changes

# 医生轮作

<<<<<<< Updated upstream
=======
# class OutPatientTimetable(db.Model):
#     __tablename__ = 'outpatienttimetable'
#     id = db.Column(db.Integer, primary_key=True)
#     doctorcycleid = db.Column(db.Integer, db.ForeignKey('doctorcycle.id'))
#     date = db.Column(db.String(128))  # 准备一个时间段与字符串数字相对应 01 -> 9:00 - 10： 00
>>>>>>> Stashed changes

# class DoctorCycle(db.Model):
#     __tablename__ = 'doctorcycle'
#     id = db.Column(db.Integer, primary_key=True)
#     doctorid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
#     classid = db.Column(db.String(64), db.ForeignKey('hospitalclass.id'))


# class OutPatientTimetable(db.Model):
#     __tablename__ = 'outpatienttimetable'
#     id = db.Column(db.Integer, primary_key=True)
#     doctorcycleid = db.Column(db.Integer, db.ForeignKey('doctorcycle.id'))
#     date = db.Column(db.String(128))  # 准备一个时间段与字符串数字相对应 01 -> 9:00 - 10： 00

<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
# class InPatientTimetable(db.Model):
#     __tablename__ = 'inpatienttimetable'
#     id = db.Column(db.Integer, primary_key=True)
#     userinfoid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
#     date = db.Column(db.String(128))

# 缺少急诊


class ExpertsTimetable(db.Model):
    __tablename__ = 'expertstimetable'
    id = db.Column(db.Integer, primary_key=True)
    userinfoid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
    cid = db.Column(db.String(64), db.ForeignKey('hospitalclass.id'))
    date = db.Column(db.Integer)


class Medicine(db.Model):
    __tablename__ = 'medicine'
    id = db.Column(db.String(128), primary_key=True)  # 6位，1开头，自增
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
    itemclass = db.Column(db.Integer, db.ForeignKey('examclass.id'))


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

class FamilyDoctorArea(db.Model):                    #家庭医生服务区域
    __tablename__ = 'fdarea'
    id = db.Column(db.String(64), primary_key=True)
    Areaname = db.Column(db.String(64))

class FamilyDoctor(db.Model):                        #创建家庭医生
    __tablename__ = 'fd'
    id = db.Column(db.String(64), primary_key=True)
    FDdoctorid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
    FDdoctorname = db.Column(db.String(64))
    FDdoctorrank = db.Column(db.Integer)
    FDdate = db.Column(db.String(128))

class FamilyDoctorWorkArea(db.Model):               #分配区域
    __tablename__ = 'fdworkarea'
    id = db.Column(db.String(64), primary_key=True)
    FDid = db.Column(db.String(64))                 #医生id
    FDareaid= db.Column(db.String(64))              #分配区域的id
    FDareaname= db.Column(db.String(64))            #分配区域的名字

class FamilyPatientInfo(db.Model):                      #家庭医生病人基本信息
    __tablename__ = 'fpinfo'
    id = db.Column(db.String(64), primary_key=True)     #病人身份证号
    FPname = db.Column(db.String(64))
    FPage = db.Column(db.Integer)
    FPsex = db.Column(db.String(64))
    FPphone = db.Column(db.String(64))

class FamilyPatientTestResult(db.Model):             #体检结果
    __tablename__ = 'fptestresult'
    id = db.Column(db.String(64), primary_key=True)
    FPid = db.Column(db.String(64))                  #病人身份证
    FPname = db.Column(db.String(64))
    FPheartrate = db.Column(db.Integer)              #心率
    FPbloodpressure = db.Column(db.Integer)          #血压
    FPresultdate = db.Column(db.String(64))          #检查日期

class SpecialConcern(db.Model):                      #特殊关注对象
    __tablename__ = 'specialconcern'
    id = db.Column(db.String(64), primary_key=True)
    SCpid = db.Column(db.String(64))
    SCpname = db.Column(db.String(64))                                      #特殊关注对象身份证 传递给门诊部
    SCpdate = db.Column(db.String(64))

class LecturePlace(db.Model):                        #家庭医生讲座地区
    __tablename__ = 'lectureplace'
    id = db.Column(db.String(64), primary_key=True)     #地区编号
    LPname = db.Column(db.String(64))

class LectureTime(db.Model):                         #家庭医生讲座安排
    __tablename__ = 'lecturetime'
    id = db.Column(db.String(64), primary_key=True)
    FDid = db.Column(db.String(64))
    LPid = db.Column(db.String(64), db.ForeignKey('lectureplace.id'))
    LPname = db.Column(db.String(64))
    LPdate = db.Column(db.String(128))


class OpCheckin(db.Model):
    __tablename__ = 'opcheckin'
<<<<<<< Updated upstream
    opcheckinid = db.Column(db.Integer, primary_key=True)
=======
    opcheckinid = db.Column(db.Integer, primary_key= True)
>>>>>>> Stashed changes
    patientid = db.Column(db.String(64), db.ForeignKey('patientinfo.id'))
    doctorid = db.Column(db.String(10), db.ForeignKey('userinfo.id'))
    doctortype = db.Column(db.Integer)
    # scsignal = db.Column(db.Integer) #与特别关注对象表对比，0为非关注，1为关注
    jips = db.Column(db.Boolean)


class OpExam(db.Model):
    __tablename__ = 'opexam'
<<<<<<< Updated upstream
    id = db.Column(db.Integer, primary_key=True)
=======
    id = db.Column(db.Integer, primary_key= True)
>>>>>>> Stashed changes
    opcheckinid = db.Column(db.Integer, db.ForeignKey('opcheckin.opcheckinid'))
    opid = db.Column(db.String(64), db.ForeignKey(
        'opcheckin.patientid'))
    examitems = db.Column(db.String(128))
<<<<<<< Updated upstream


class OpCheck(db.Model):
    __tablename__ = 'opcheck'
    id = db.Column(db.Integer, primary_key=True)
=======

class OpCheck(db.Model):
    __tablename__ = 'opcheck'
    id = db.Column(db.Integer, primary_key= True)
>>>>>>> Stashed changes
    opcheckinid = db.Column(db.Integer, db.ForeignKey('opcheckin.opcheckinid'))
    opid = db.Column(db.String(64), db.ForeignKey(
        'opcheckin.patientid'))
    checkitems = db.Column(db.String(128))


class OpRecipe(db.Model):
    __tablename__ = 'oprecipe'
<<<<<<< Updated upstream
    id = db.Column(db.Integer, primary_key=True)
=======
    id = db.Column(db.Integer, primary_key= True)
>>>>>>> Stashed changes
    opcheckinid = db.Column(db.Integer, db.ForeignKey('opcheckin.opcheckinid'))
    opid = db.Column(db.String(64), db.ForeignKey(
        'opcheckin.patientid'))
    medicinenames = db.Column(db.String(128))
    medicinenumbers = db.Column(db.String(128))


class OpCheckinAfford(db.Model):
    __tablename__ = 'opcheckinafford'
<<<<<<< Updated upstream
    id = db.Column(db.Integer, primary_key=True)
=======
    id = db.Column(db.Integer, primary_key= True)
>>>>>>> Stashed changes
    opcheckinid = db.Column(db.Integer, db.ForeignKey('opcheckin.opcheckinid'))
    opid = db.Column(db.String(64), db.ForeignKey(
        'opcheckin.patientid'))
    price = db.Column(db.Float)


class OpExamAfford(db.Model):
    __tablename__ = 'opexamafford'
<<<<<<< Updated upstream
    id = db.Column(db.Integer, primary_key=True)
=======
    id = db.Column(db.Integer, primary_key= True)
>>>>>>> Stashed changes
    opcheckinid = db.Column(db.Integer, db.ForeignKey('opcheckin.opcheckinid'))
    opid = db.Column(db.String(64), db.ForeignKey(
        'opcheckin.patientid'))
    price = db.Column(db.Float)


class OpCheckAfford(db.Model):
    __tablename__ = 'opcheckafford'
<<<<<<< Updated upstream
    id = db.Column(db.Integer, primary_key=True)
=======
    id = db.Column(db.Integer, primary_key= True)
>>>>>>> Stashed changes
    opcheckinid = db.Column(db.Integer, db.ForeignKey('opcheckin.opcheckinid'))
    opid = db.Column(db.String(64), db.ForeignKey(
        'opcheckin.patientid'))
    price = db.Column(db.Float)


class OpRecipeAfford(db.Model):
    __tablename__ = 'oprecipeafford'
<<<<<<< Updated upstream
    id = db.Column(db.Integer, primary_key=True)
=======
    id = db.Column(db.Integer, primary_key= True)
>>>>>>> Stashed changes
    opcheckinid = db.Column(db.Integer, db.ForeignKey('opcheckin.opcheckinid'))
    opid = db.Column(db.String(64), db.ForeignKey(
        'opcheckin.patientid'))
    price = db.Column(db.Float)

<<<<<<< Updated upstream

class OpCost(db.Model):
    __tablename__ = 'opcost'
    opcheckinid = db.Column(db.Integer, db.ForeignKey(
        'opcheckin.opcheckinid'), primary_key=True)
    cost = db.Column(db.Float)


class InPatientDeposit(db.Model):
    __tablename__ = 'inpatientdeposit'
    id = db.Column(db.Integer, db.ForeignKey(
        'opcheckin.opcheckinid'), primary_key=True)
    patientid = db.Column(db.String(64), db.ForeignKey(
        'patientinfo.id'), primary_key=True)
    rest = db.Column(db.Float)
    totalcost = db.Column(db.Float)
    ischeck = db.Column(db.Boolean)


class InPatientTableSet(db.Model):
    __tablename__ = 'inpatienttableset'
    id = db.Column(db.Integer, db.ForeignKey(
        'inpatientdeposit.id'), primary_key=True)
    inpatienttimeandbedid = db.Column(db.String(128))
    inpatientcheckid = db.Column(db.String(128))
    inpatientinspectid = db.Column(db.String(128))
    inpatientprescriptid = db.Column(db.String(128))


class InPatientTimeAndBed(db.Model):
    __tablename__ = 'inpatienttimeandbed'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tableid = db.Column(db.Integer, db.ForeignKey(
        'inpatienttableset.id'))
    bedid = db.Column(db.Integer, db.ForeignKey('bedinfo.id'))
    doctorinfoid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)


class InPatientCheck(db.Model):
    __tablename__ = 'inpatientcheck'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tableid = db.Column(db.Integer, db.ForeignKey(
        'inpatienttableset.id'))
    checkitemsid = db.Column(db.String(128))
    doctorinfoid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
    cost = db.Column(db.Float)


class InPatientInspect(db.Model):
    __tablename__ = 'inpatientinspect'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tableid = db.Column(db.Integer, db.ForeignKey(
        'inpatienttableset.id'))
    inspectitemsid = db.Column(db.String(128))
    doctorinfoid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
    cost = db.Column(db.Float)


class InPatientPrescript(db.Model):
    __tablename__ = 'inpatientprescript'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tableid = db.Column(db.Integer, db.ForeignKey(
        'inpatienttableset.id'))
    medicineid = db.Column(db.String(128))
    medicinenumbers = db.Column(db.String(128))
    doctorinfoid = db.Column(db.String(64), db.ForeignKey('userinfo.id'))
    cost = db.Column(db.Float)

class ImgpCheckin(db.Model):
    __tablename__ = 'imgpcheckin'
    imgpcheckinid = db.Column(db.Integer, primary_key= True)
    patientid = db.Column(db.String(64), db.ForeignKey('patientinfo.id'))
    doctorid = db.Column(db.String(10), db.ForeignKey('userinfo.id'))
    doctortype = db.Column(db.Integer)
    # scsignal = db.Column(db.Integer) #与特别关注对象表对比，0为非关注，1为关注
    # jips = db.Column(db.Boolean)

class ImgpRecipe(db.Model):
    __tablename__ = 'imgprecipe'
    id = db.Column(db.Integer, primary_key= True)
    imgpcheckinid = db.Column(db.Integer, db.ForeignKey('imgpcheckin.imgpcheckinid'))
    imgpid = db.Column(db.String(64), db.ForeignKey(
        'imgpcheckin.patientid'))
    medicinenames = db.Column(db.String(128))
    medicinenumbers = db.Column(db.String(128))

class ImgpCheckinAfford(db.Model):
    __tablename__ = 'imgpcheckinafford'
    id = db.Column(db.Integer, primary_key= True)
    imgpcheckinid = db.Column(db.Integer, db.ForeignKey('imgpcheckin.imgpcheckinid'))
    imgpid = db.Column(db.String(64), db.ForeignKey(
        'imgpcheckin.patientid'))
    price = db.Column(db.Float)

class ImgpRecipeAfford(db.Model):
    __tablename__ = 'imgprecipeafford'
    id = db.Column(db.Integer, primary_key= True)
    imgpcheckinid = db.Column(db.Integer, db.ForeignKey('imgpcheckin.imgpcheckinid'))
    imgpid = db.Column(db.String(64), db.ForeignKey(
        'imgpcheckin.patientid'))
    price = db.Column(db.Float)

class ImgpCost(db.Model):
    __tablename__ = 'imgpcost'
    imgpcheckinid = db.Column(db.Integer, db.ForeignKey('imgpcheckin.imgpcheckinid'), primary_key= True)
    cost = db.Column(db.Float)
=======
class OpCost(db.Model):
    __tablename__ = 'opcost'
    opcheckinid = db.Column(db.Integer, db.ForeignKey('opcheckin.opcheckinid'), primary_key= True)
    cost = db.Column(db.Float)
>>>>>>> Stashed changes
