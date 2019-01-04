from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from model import AdminTable, UserGroup

class FDpatientinfo(FlaskForm):
    FPid = StringField('身份证', validtors=[
        DataRequired(), Length(16,18), Regexp('^[0-9Xx]*$', 0, '身份证必须是数字或者大小写X')
    ])
    FPname = StringField('姓名', validtors=[
        DataRequired(), Length(1,64), Regexp('^[u4e00-u9fa5]+$', 0, '用户名必须是中文字符')
    ])
    FPheartrate = StringField('心率', validtors=[
        DataRequired(), Length(1,64), Regexp('^[0-9]*$', 0,'')
    ])
    FPbloodpressure = StringField('血压', validtors=[
        DataRequired(), Length(1,64), Regexp('^[0-9]*$', 0,'')
    ])

    

class FDcreate(FlaskForm):


class (FlaskForm):
