from flask import Blueprint

inpatient = Blueprint('inpatient', __name__)  # 设定蓝本的名称

from .import views