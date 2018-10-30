from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from model import AdminTable, UserGroup
from wtforms import ValidationError
from ..models import Role, User
from flask_pagedown.fields import PageDownField

class FDpatientinfo(FlaskForm):
    FPid = StringField('身份证', validtors=[
        DataRequired(), Length(16,18), Regexp('^[0-9Xx]*$', 0, '身份证必须是数字或者大小写X')
    ])
    FPname = StringField('姓名', validtors=[
        DataRequired(), Length(1,64), Regexp('^[u4e00-u9fa5]+$', 0, '用户名必须是中文字符')
    ])
    FPsex = StringField('性别', validtors=[
        DataRequired(), Length(1,32), Regexp('^[u4e00-u9fa5]+$', 0, '')
    ])
    FPsex = StringField('年龄', validtors=[
        DataRequired(), Length(1,32), Regexp('^[0-9]*$', 0, '年龄必须是数字')
    ])
    FPphone= StringField('联系电话', validtors=[
        DataRequired(), Length(1,32), Regexp('^[0-9]*$', 0, '号码必须是数字')
    ])
    submit = SubmitField('上传病人基本信息')



class FDTR(FlaskForm):
    FPid = StringField('病患号码', validtors=[
        DataRequired(), Length(1,32), Regexp('^[0-9]*$', 0,'')
    ])
    FPid = StringField('病患姓名', validtors=[
        DataRequired(), Length(1,32), Regexp('^^[u4e00-u9fa5]+$', 0,'')
    ])
    FPheartrate = StringField('心率', validtors=[
        DataRequired(), Length(1,32), Regexp('^[0-9]*$', 0,'')
    ])
    FPbloodpressure = StringField('血压', validtors=[
        DataRequired(), Length(1,32), Regexp('^[0-9]*$', 0,'')
    ])
    sumbit = SubmitField('上传体检结果')



class FD(FlaskForm)