from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField, ValidationError, DateField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from ..model import InPatientTableSet, InPatientCheck, InPatientInspect, InPatientPrescript, InPatientTimeAndBed


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
    checkitemsid = StringField('检查项目列表')
