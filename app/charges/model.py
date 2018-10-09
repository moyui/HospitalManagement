from . import db

class InPatientDeposit(db.model):
    __tablename__ = 'inpatientdeposit'
    id = db.Column(db.Integer, primary_key=True)
    patientid = db.Column(db.String(10), db.ForeignKey('opcheckin.id'))
    rest = db.Column(db.Float)

class InPatientTotalCost(db.model):
    __tablename__ = 'inpatienttotalcost'
    id = db.Column(db.Integer, primary_key=True)
    patientid = db.Column(db.String(10), db.ForeignKey('opcheckin.id'))
    totalcost = db.Column(db.Float)
    unpaiditemsid = db.Column(db.String(64)) #未支付项