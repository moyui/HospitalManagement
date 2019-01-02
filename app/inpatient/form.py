from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField, ValidationError, DateField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from ..model import InPatientTableSet, InPatientCheck, InPatientInspect, InPatientPrescript, InPatientTimeAndBed


class InPatientLoginFrom(FlaskForm):
    patientid = StringField('身份证', validators=[
        DataRequired(), Length(16, 18), Regexp(
            '^[0-9Xx]*$', 0, '身份证必须是数字或者大小写X')
    ])
    submit = SubmitField('查询')

    # def __init__(self, patientid, name, age, sex, nodata, *args, **kwargs):
    #     super(InPatientLoginFrom, self).__init__(*args, **kwargs)
    #     if patientid is not None and name is not None and age is not None and sex is not None:
    #         self.patientid = patientid
    #         self.name = name
    #         self.age = age
    #         self.sex = sex



class InPatientTimeForm(FlaskForm):
    startDate = DateField('开始日期')
    endDate = DateField('结束日期')
    bedId = StringField('床号')
    submit = SubmitField('提交')


class InPatientCheckForm(FlaskForm):
    checkitemsid = StringField('检查项目列表')
