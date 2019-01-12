from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, EqualTo


class PreChargeCheckForm(FlaskForm):
    id = StringField('身份证')
    submit = SubmitField('确认')


class PreChargePayForm(FlaskForm):
    id = StringField('身份证', render_kw={'readonly': True})
    name = StringField('姓名', render_kw={'readonly': True})
    age = StringField('年龄', render_kw={'readonly': True})
    sex = StringField('性别', render_kw={'readonly': True})
    precharge = StringField('押金/充值', validators=[
        DataRequired(), Regexp('^[0-9]+$', 0, '输入必须是数字')
    ])
    submit = SubmitField('确认')

class PreChargeLoginFrom(FlaskForm):
    patientid = StringField('身份证', validators=[
        DataRequired(), Length(16, 18), Regexp(
            '^[0-9Xx]*$', 0, '身份证必须是数字或者大小写X')
    ])
    name = StringField('姓名', render_kw={'readonly': True})
    age = StringField('年龄', render_kw={'readonly': True})
    sex = StringField('性别', render_kw={'readonly': True})
    submit = SubmitField('查询')

