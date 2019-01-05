from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField, ValidationError, DateField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from ..model import InPatientTableSet, InPatientCheck, InPatientInspect, InPatientPrescript, InPatientTimeAndBed, ExamItem, CheckItem, Medicine


class InPatientLoginFrom(FlaskForm):
    patientid = StringField('身份证', validators=[
        DataRequired(), Length(16, 18), Regexp(
            '^[0-9Xx]*$', 0, '身份证必须是数字或者大小写X')
    ])
    name = StringField('姓名', render_kw={'readonly': True})
    age = StringField('年龄', render_kw={'readonly': True})
    sex = StringField('性别', render_kw={'readonly': True})
    submit = SubmitField('查询')


class InPatientTableSetFrom(FlaskForm):
    id = StringField('身份证', render_kw={'readonly': True})
    submit = SubmitField('创建')


class InPatientCloseBedForm(FlaskForm):
    bedId = StringField('床号', render_kw={'readonly': True})
    startDate = DateField('开始日期', render_kw={'readonly': True})
    endDate = DateField('结束日期')
    submit = SubmitField('结束病床')


class InPatientNewBedForm(FlaskForm):
    bedId = StringField('床号')
    submit = SubmitField('提交')


class InPatientCheckForm(FlaskForm):
    opid = StringField('单号', render_kw={'readonly': True})
    checkitems = SelectMultipleField('检查项目', widget=widgets.ListWidget(
        prefix_label=False), option_widget=widgets.CheckboxInput())
    submit = SubmitField('确定')

    def __init__(self, *args, **kwargs):
        super(OpCheckForm, self).__init__(*args, **kwargs)
        checklist = CheckItem.query.with_entities(
            CheckItem.checkitemname).all()
        checknum = []
        for i in range(len(checklist)):
            checknum.append(i+1)
        zipped = zip(checknum, checklist)
        self.checkitems.choices = zipped


class InPatientInspectForm(FlaskForm):
    opid = StringField('单号', render_kw={'readonly': True})
    examitems = SelectMultipleField('检验项目', widget=widgets.ListWidget(
        prefix_label=False), option_widget=widgets.CheckboxInput())
    submit = SubmitField('确定')

    def __init__(self, *args, **kwargs):
        super(OpExamForm, self).__init__(*args, **kwargs)
        examlist = ExamItem.query.with_entities(
            ExamItem.id, ExamItem.examitemname).all()
        examnum = []
        for i in range(len(examlist)):
            examnum.append(i+1)
        zipped = zip(examnum, examlist)
        self.examitems.choices = examlist

class InpatientPrescriptForm(FlaskForm):
    opid = StringField('单号', render_kw={'readonly': True})
    medicineitems = SelectMultipleField('处方项目', widget=widgets.ListWidget(
        prefix_label=False), option_widget=widgets.CheckboxInput())
    submit = SubmitField('确定')

    def __init__(self, *args, **kwargs):
        super(OpExamForm, self).__init__(*args, **kwargs)
        medicinelist = Medicine.query.with_entities(
            Medicine.id, Medicine.medicinename).all()
        medicinenum = []
        for i in range(len(medicinelist)):
            medicinenum.append(i+1)
        zipped = zip(medicinenum, medicinelist)
        self.medicineitems.choices = zipped

