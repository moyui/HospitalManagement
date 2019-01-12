from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField, ValidationError, DateField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from ..model import InPatientTableSet, InPatientCheck, InPatientInspect, InPatientPrescript, InPatientTimeAndBed, ExamItem, CheckItem, Medicine, BedInfo


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
    endDate = DateField('结束日期', render_kw={'readonly': True})
    submit = SubmitField('结束病床')


class InPatientNewBedForm(FlaskForm):
    bedlist = SelectField('床号')
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(InPatientNewBedForm, self).__init__(*args, **kwargs)
        beditems = BedInfo.query.filter_by(isused=False).all()
        bedlist = []
        for i in beditems:
            bedlist.append((i.id, '%s区%s号'%(i.areaid, i.id)))
        self.bedlist.choices = bedlist

class InPatientCheckForm(FlaskForm):
    opid = StringField('患者号', render_kw={'readonly': True})
    checkitems = SelectMultipleField('检查项目', widget=widgets.ListWidget(
        prefix_label=False), option_widget=widgets.CheckboxInput())
    submit = SubmitField('确定')

    def __init__(self, *args, **kwargs):
        super(InPatientCheckForm, self).__init__(*args, **kwargs)
        checklist = CheckItem.query.with_entities(CheckItem.id, CheckItem.checkitemname).all()
        self.checkitems.choices = checklist


class InPatientInspectForm(FlaskForm):
    opid = StringField('患者号', render_kw={'readonly': True})
    examitems = SelectMultipleField('检验项目', widget=widgets.ListWidget(
        prefix_label=False), option_widget=widgets.CheckboxInput())
    submit = SubmitField('确定')

    def __init__(self, *args, **kwargs):
        super(InPatientInspectForm, self).__init__(*args, **kwargs)
        examlist = ExamItem.query.with_entities(ExamItem.id, ExamItem.examitemname).all()
        self.examitems.choices = examlist 

class InpatientPrescriptForm(FlaskForm):
    opid = StringField('患者号', render_kw={'readonly': True})
    medicines = SelectMultipleField('药品', widget= widgets.ListWidget(prefix_label=False), option_widget= widgets.CheckboxInput())
    submit = SubmitField('确定')

    def __init__(self, *args, **kwargs):
        super(InpatientPrescriptForm, self).__init__(*args, **kwargs)
        medicinelist = Medicine.query.with_entities(Medicine.id, Medicine.medicinename).all()
        self.medicines.choices = medicinelist
