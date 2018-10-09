from . import db

class InPatientTableSet(db.model):
    __tablename__ = 'inpatienttableset'
    id = db.Column(db.String(64), db.ForeignKey('inpatientdeposit.id'), primary_key=True)
    patientid = db.Column(db.String(10), db.ForeignKey('opcheckin.id'))
    doctorid = db.Column(db.String(64), db.ForeignKey('inpatienttimetable.id'))
    inpatienttimeandbedid = db.Column(db.String(128))
    inpatientcheckid = db.Column(db.String(128))
    inpatientinspectid = db.Column(db.String(128))
    inpatientprescriptid = db.Column(db.String(128))

class InPatientTimeAndBed(db.model):
    __tablename__ = 'inpatienttimeandbed'
    id = db.Column(db.String(64), primary_key=True)
    badid = db.Column(db.String(64), db.ForeignKey('bedinfo.id')) #待填写
    doctorinfoid = db.Column(db.String(64), db.ForeignKey('doctorinfo.id'))
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)

class InPatientCheck(db.model):
    __tablename__ = 'inpatientcheck'
    id = db.Column(db.String(64), primary_key=True)
    checkitemsid = db.Column(db.String(128))
    doctorinfoid = db.Column(db.String(64), db.ForeignKey('doctorinfo.id'))

class InPatientInspect(db.model):
    __tablename__ = 'inpatientinspect'
    id = db.Column(db.String(64), primary_key=True)
    inspectitemsid = db.Column(db.String(128))
    doctorinfoid = db.Column(db.String(64), db.ForeignKey('doctorinfo.id'))

class InPatientPrescript(db.model):
    __tablename__ = 'inpatientprescript'
    id = db.Column(db.String(64), primary_key=True)
    prescriptitemsid = db.Column(db.String(128))
    doctorinfoid = db.Column(db.String(64), db.ForeignKey('doctorinfo.id'))