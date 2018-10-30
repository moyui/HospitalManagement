from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from .model import InPatientTableSet, InPatientCheck, InPatientInspect, InPatientPrescript, InPatientTimeAndBed

class 