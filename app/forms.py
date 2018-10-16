from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from model import AdminTable, UserGroup

class RegisterFrom(FlaskForm):
    idcard = StringField('身份证', validators=[
        DataRequired(), Length(16, 18), Regexp('^[0-9Xx]*$', 0, '身份证必须是数字或者大小写X')
    ])
    name = StringField('用户名', validators=[
        DataRequired(), Length(1, 64), Regexp('^[u4e00-u9fa5]+$', 0, '用户名必须是中文字符')])
    password = PasswordField('密码', validators=[
        DataRequired(), EqualTo('password2', message='两次输入的密码必须一致')])
    password2 = PasswordField('确认密码',validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate(self, field):
        if AdminTable.query.filter_by(idcard=field.data).first():
            raise ValidationError('该用户身份证已经被注册。')