from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from .model import InPatientDeposit, InPatientTotalCost

class PreChargeForm(FlaskForm):
    id = StringField('身份证')
    name = StringField('姓名')
    precharge = StringField('押金', validators=[
        DataRequired(), Regexp('^[0-9]+$', 0, '输入必须是数字')
    ])

    def __init__(self, id, name, *args, **kwargs):
        super(PreChargeForm, self).__init__(*args, **kwargs)
        self.id = id
        self.name = name