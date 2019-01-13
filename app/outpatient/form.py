from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, SelectMultipleField, widgets, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from ..model import OpCheckin, ExamItem, CheckItem, Medicine, DoctorTimetable, ExpertsTimetable, UserInfo
from datetime import datetime

class OpCheckinForm(FlaskForm):
    doctorname = SelectField('医生姓名', widget= widgets.ListWidget(prefix_label=False), option_widget= widgets.CheckboxInput())
    submit = SubmitField('确定')

    def __init__(self, *args, **kwargs):
        super(OpCheckinForm, self).__init__(*args, **kwargs)
        d = datetime.now()
        dw = d.weekday()
        dn = []
        did =[]
        en = []
        eid = []
        # print(dw)
        doctorinfo = DoctorTimetable.query.filter_by(doctortime= dw).all()
        expertinfo = ExpertsTimetable.query.filter_by(date= dw).all()
        for i in doctorinfo:
            dname = UserInfo.query.filter_by(id= i.doctorid).all()
            did.append(i.doctorid)
            for j in dname:
                dstr = '门诊医生:%s' % j.name
                dn.append(dstr)
        for i in expertinfo:
            ename = UserInfo.query.filter_by(id= i.userinfoid).all()
            did.append(i.userinfoid)
            for j in ename:
                estr = '专家:%s' % j.name
                dn.append(estr)
        a = zip(did, dn)
        for i in a:
            print(i)
        self.doctorname.choices = zip(did, dn)

class OpCheckinTwoForm(FlaskForm):
    submit = SubmitField('确认提交')

class OpExamForm(FlaskForm):
    examitems = SelectMultipleField('检验项目', widget= widgets.ListWidget(prefix_label=False), option_widget= widgets.CheckboxInput())
    submit = SubmitField('确定')

    def __init__(self, *args, **kwargs):
        super(OpExamForm, self).__init__(*args, **kwargs)
        examlist = ExamItem.query.with_entities(ExamItem.id, ExamItem.examitemname).all()
        print(examlist)
        self.examitems.choices = examlist 

class OpCheckForm(FlaskForm):
    checkitems = SelectMultipleField('检查项目', widget= widgets.ListWidget(prefix_label=False), option_widget= widgets.CheckboxInput())
    submit = SubmitField('确定')

    def __init__(self, *args, **kwargs):
        super(OpCheckForm, self).__init__(*args, **kwargs)
        checklist = CheckItem.query.with_entities(CheckItem.id, CheckItem.checkitemname).all()
        self.checkitems.choices = checklist
    
class OpRecipeForm(FlaskForm):
    medicines = SelectMultipleField('药品', widget= widgets.ListWidget(prefix_label=False), option_widget= widgets.CheckboxInput())
    submit = SubmitField('确定')

    def __init__(self, *args, **kwargs):
        super(OpRecipeForm, self).__init__(*args, **kwargs)
        medicinelist = Medicine.query.with_entities(Medicine.id, Medicine.medicinename).all()
        self.medicines.choices = medicinelist

class OpIndexForm(FlaskForm):
    inpatientcheck = BooleanField('住院')
    submit = SubmitField('确定')

class OpSearchForm(FlaskForm):
    opcheckinid = StringField('请输入您的门诊挂号单号')
    submit = SubmitField('查询')

class OpCostListForm(FlaskForm):
    opcheckinid = StringField('请输入您的门诊挂号单号')
    submit = SubmitField('查询')

class OpExitForm(FlaskForm):
    submit = SubmitField('注销')