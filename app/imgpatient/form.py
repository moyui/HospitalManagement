from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, SelectMultipleField, widgets, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from ..model import ImgpCheckin, Medicine, ImgDoctorTimetable, UserInfo
from datetime import datetime

class ImgpCheckinForm(FlaskForm):
    patientid = StringField('身份证', validators=[DataRequired(), Length(8, 20), Regexp('^[0-9Xx]*$', 0, '身份证必须是数字或者大小写X')])
    doctorname = SelectField('医生姓名', widget= widgets.ListWidget(prefix_label=False), option_widget= widgets.CheckboxInput())
    submit = SubmitField('确定')

    def __init__(self, *args, **kwargs):
        super(ImgpCheckinForm, self).__init__(*args, **kwargs)
        d = datetime.now()
        dw = d.weekday()
        dn = []
        did =[]
        # en = []
        # eid = []
        # print(dw)
        doctorinfo = ImgDoctorTimetable.query.filter_by(doctortime= dw).all()
        # expertinfo = ExpertsTimetable.query.filter_by(date= dw).all()
        for i in doctorinfo:
            dname = UserInfo.query.filter_by(id= i.doctorid).all()
            did.append(i.doctorid)
            for j in dname:
                dstr = j.name
                dn.append(dstr)
        # for i in expertinfo:
        #     ename = UserInfo.query.filter_by(id= i.userinfoid).all()
        #     did.append(i.userinfoid)
        #     for j in ename:
        #         estr = '专家:%s' % j.name
        #         dn.append(estr)
        # a = zip(did, dn)
        # for i in a:
        #     print(i)
        self.doctorname.choices = zip(did, dn)

class ImgpRecipeForm(FlaskForm):
    imgpid = StringField('患者号', validators=[DataRequired(), Length(8, 20), Regexp('^[0-9Xx]*$', 0, '患者号必须是数字或者大小写X')])
    medicines = SelectMultipleField('药品', widget= widgets.ListWidget(prefix_label=False), option_widget= widgets.CheckboxInput())
    submit = SubmitField('确定')

    def __init__(self, *args, **kwargs):
        super(ImgpRecipeForm, self).__init__(*args, **kwargs)
        medicinelist = Medicine.query.with_entities(Medicine.id, Medicine.medicinename).all()
        self.medicines.choices = medicinelist