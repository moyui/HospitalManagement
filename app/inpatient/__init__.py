from flask import Blueprint

inpatient = Blueprint('charges', __name__)#设定蓝本的名称

from . import views