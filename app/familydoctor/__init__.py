from flask import Blueprint

familydoctor = Blueprint('familydoctor', __name__)  # 设定蓝本的名称

from .import views