from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField, ValidationError, DateField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from ..model import FamilyDoctorArea, FamilyDoctor, FamilyDoctorWorkArea, FamilyPatientInfo, FamilyPatientTestResult, SpecialConcern, LecturePlace, LectureTime

class FamilyPatientInfoForm(FlaskForm):                    #病人登记
    patientid = StringField('身份证', validators=[
        DataRequired(), Length(16, 18), Regexp(
            '^[0-9Xx]*$', 0, '身份证必须是数字或者大小写X')
    ])
    name = StringField('病人姓名')
    sex = StringField('性别')
    age = StringField('年龄')
    phone = StringField('联系电话')
    submit = SubmitField('病人登记')

class TestResultForm(FlaskForm):                            #病人体检结果填写
    patientid = StringField('身份证', validators=[
        DataRequired(), Length(16, 18), Regexp(
            '^[0-9Xx]*$', 0, '身份证必须是数字或者大小写X')
    ])
    name = StringField('病人姓名')
    fpheartrate = StringField('心率')
    fpbloodpressure = StringField('血压')
    resultdate = StringField('检查日期 示例<2019.1.10>')
    submit = SubmitField('提交')

class SCListForm(FlaskForm):
    listdate = StringField('输入要添加的日期 示例<2019.1.10>')
    submit = SubmitField('添加特殊关注对象')

class FDCreateForm(FlaskForm):
    submit = SubmitField('更新家庭医生安排')

class FDAreaForm(FlaskForm):
    areaid = StringField('区域id')
    areaname = StringField('区域名字')
    submit = SubmitField('提交')

class FDLectureForm(FlaskForm):
    lecid = StringField('讲座区域id')
    lecname = StringField('讲座区域名字')
    submit = SubmitField('提交')

class FDdelete(FlaskForm):
    fddid = StringField('你想删除的家庭医生的医生id')
    submit = SubmitField('提交')

class FamilyDoctorShow(FlaskForm):
    submit = SubmitField('查看')

class FamilyDoctorWorkShow(FlaskForm):
    submit = SubmitField('查看')

class FamilyDoctorLecturekShow(FlaskForm):
    submit = SubmitField('查看')

class FamilyDoctorpinfoshow(FlaskForm):
    patientid = StringField('身份证', validators=[
    DataRequired(), Length(16, 18), Regexp(
    '^[0-9Xx]*$', 0, '身份证必须是数字或者大小写X')
    ])
    submit = SubmitField('查看')






