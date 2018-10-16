from . import db

class OpCheckin(db.Model):
    __tablename__ = 'opcheckin'
    id = db.Column(db.String(10), primary_key=True)
    patientid = db.Column(db.String(10), db.ForeignKey('patientinfo.id'))
    doctorid = db.Column(db.String(10), db.ForeignKey('doctorinfo.id'))
    doctime = db.Column(db.Integer, db.ForeignKey('outpatienttimetable.id'))
    experttime = db.Column(db.Integer, db.ForeignKey('expertstimetable.id'))
    scsignal = db.Column(db.Integer) #与特别关注对象表对比，0为非关注，1为关注
    jips = db.Column(db.Boolean)

class OpExam(db.Model):
    __tablename__ = 'opexam'
    id = db.Column(db.String(10), db.ForeignKey('opcheckin.id'))
    examitems = db.Column(db.String(128), db.ForeignKey('examitem.id'))

class OpCheck(db.Model):
    __tablename__ = 'opcheck'
    id = db.Column(db.String(10), db.ForeignKey('opcheckin.id'))
    checkitems = db.Column(db.String(128), db.ForeignKey('checkitem.id'))

class OpRecipe(db.Model):
    __tablename__ = 'oprecipe'
    id = db.Column(db.String(10), db.ForeignKey('opcheckin.id'))
    medicinenames = db.Column(db.String(128))

class OpCheckinAfford(db.Model):
    __tablename__ = 'opcheckinafford'
    id = db.Column(db.String(10), db.ForeignKey('opcheckin.id'))
    price = db.Column(db.Float)

class OpExamAfford(db.Model):
    __tablename__ = 'opexamafford'
    id = db.Column(db.String(10), db.ForeignKey('opcheckin.id'))
    price = db.Column(db.Float)

class OpCheckAfford(db.Model):
    __tablename__ = 'opcheckafford'
    id = db.Column(db.String(10),db.ForeignKey('opcheckin.id'))
    price = db.Column(db.Float)

class OpRecipeAfford(db.Model):
    __tablename__ = 'oprecipeafford'
    id = db.Column(db.String(10), db.ForeignKey('openchecin.id'))
    price = db.Column(db.Float)