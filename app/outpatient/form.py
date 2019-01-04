from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from ..model import OpCheckin, ExamItem, CheckItem

class OpCheckinForm(FlaskForm):
    patientid = StringField('身份证', validators=[DataRequired(), Length(16, 18), Regexp('^[0-9Xx]*$', 0, '身份证必须是数字或者大小写X')])
    doctorname = StringField('医生姓名')
    expertname = StringField('专家姓名')

    def __init__(self, doctorname, expertname, *args, **kwargs):
        super(OpCheckinForm, self).__init__(*args, **kwargs)


class OpExamForm(FlaskForm):
    opid = StringField('患者号', validators=[DataRequired(), Length(8, 9), Regexp('^[0-9Xx]*$', 0, '患者号必须是数字或者大小写X')])
    examitems = SelectMultipleField('检验项目', widget= widgets.ListWidget(prefix_label=False), option_widget= widgets.CheckboxInput())
    submit = SubmitField('确定')
    print(examitems)

    def __init__(self, *args, **kwargs):
        super(OpExamForm, self).__init__(*args, **kwargs)
        examlist = ExamItem.query.with_entities(ExamItem.id, ExamItem.examitemname).all()
        print(examlist)
        # examnum = []
        # for i in range(len(examlist)):
        #     examnum.append(i+1)
        # zipped = zip(examnum, examlist)
        self.examitems.choices = examlist 

class OpCheckForm(FlaskForm):
    opid = SelectField('患者号', validators=[DataRequired(), Length(16, 18), Regexp('^[0-9Xx]*$', 0, '患者号必须是数字或者大小写X')])
    checkitems = SelectMultipleField('检查项目', widget= widgets.ListWidget(prefix_label=False), option_widget= widgets.CheckboxInput())
    submit = SubmitField('确定')

    def __init__(self, *args, **kwargs):
        super(OpCheckForm, self).__init__(*args, **kwargs)
        checklist = CheckItem.query.with_entities(CheckItem.checkitemname).all()
        checknum = []
        for i in range(len(checklist)):
            checknum.append(i+1)
        zipped = zip(checknum, checklist)
        self.checkitems.choices = zipped