from flask import Flask, render_template
from flask_wtf import Form
from wtforms import BooleanField
from wtforms.validators import DataRequired
 
app = Flask(__name__)
app.secret_key = 'STACKOVERFLOW'

class ExampleForm(Form):
    checkbox = BooleanField('Agree?', validators=[DataRequired(), ])  #这是主要用法
 
@app.route('/', methods=['post', 'get'])
def home():

    form = ExampleForm()
    if form.validate_on_submit():
        return str(form.checkbox.data)
    else:
        return render_template('example.html', form=form)
 
 
if __name__ == '__main__':
    app.run(debug=True, port=5060)