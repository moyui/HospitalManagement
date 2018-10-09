from . import db

class InPatientDeposit(db.model):
    __tablename__ = 'inpatientdeposit'
    id = db.Column(db.Integer, primary_key=True)
    rest = db.Column(db.Float)

class InPatientTotalCost(db.model):
    __tablename__ = 'inpatienttotalcost'
    id = db.Column(db.Integer, primary_key=True)
    totalcost = db.Column(db.Float)
    unpaiditemsid = db.Column(db.String(64)) #未支付项

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