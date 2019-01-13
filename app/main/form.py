from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo

class Exit(FlaskForm):
    submit = SubmitField('登出')

class PatientInfoForm(FlaskForm):
    patientid = StringField('身份证', validators=[DataRequired(), Length(8, 20), Regexp('^[0-9Xx]*$', 0, '身份证必须是数字或者大小写X')])
    name = StringField('姓名')
    birth = StringField('出生日期')
    sex = SelectField(label= '性别', choices= [(1, '男'), (0, '女')], coerce= int)
    age = StringField('年龄')
    submit = SubmitField('提交信息')