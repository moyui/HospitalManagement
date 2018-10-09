from . import db

class InPatientTableSet(db.model):
    __tablename__ = 'inpatienttableset'
    id = db.Column(db.Integer, db.ForeignKey('inpatientdeposit.id'), primary_key=True)
    patientid = db.Column(db.String(64))
    inpatienttimeandbedid = db.Column(db.Integer)
    inpatientcheckid = db.Column(db.Integer)
    inpatientinspectid = db.Column(db.Integer)
    inpatientprescriptid = db.Column(db.Integer)

class InPatientTimeAndBed(db.model):
    __tablename__ = 'inpatienttimeandbed'
    id = db.Column(db.Integer, primary_key=True)
    tablesetid = db.Column(db.Integer, db.ForeignKey('inpatienttableset.inpatienttimeandbedid'), primary_key=True)
    badid = db.Column(db.Integer, db.ForeignKey('')) #待填写
    doctorinfoid = db.Column(db.String(64), db.ForeignKey('doctorinfo.id'))
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)

class InPatientCheck(db.model):
    __tablename__ = 'inpatientcheck'
    id = db.Column(db.Integer, primary_key=True)
    tablesetid = db.Column(db.Integer, db.ForeignKey('inpatienttableset.inpatientcheckid'), primary_key=True)
    checkitemsid = db.Column(db.String(64)) #需要讨论
    doctorinfoid = db.Column(db.String(64), db.ForeignKey('doctorinfo.id'))

class InPatientInspect(db.model):
    __tablename__ = 'inpatientinspect'
    id = db.Column(db.Integer, primary_key=True)
    tablesetid = db.Column(db.Integer, db.ForeignKey('inpatienttableset.inpatientinspectid'), primary_key=True)
    inspectitemsid = db.Column(db.String(64))
    doctorinfoid = db.Column(db.String(64), db.ForeignKey('doctorinfo.id'))

class InPatientPrescript(db.model):
    __tablename__ = 'inpatientprescript'
    id = db.Column(db.Integer, primary_key=True)
    tablesetid = db.Column(db.Integer, db.ForeignKey('inpatienttableset.inpatientprescriptid'), primary_key=True)
    prescriptitemsid = db.Column(db.String(64))
    doctorinfoid = db.Column(db.String(64), db.ForeignKey('doctorinfo.id'))