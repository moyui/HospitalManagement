from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo

class Exit(FlaskForm):
    submit = SubmitField('登出')