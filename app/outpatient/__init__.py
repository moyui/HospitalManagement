from flask import Blueprint

outpatient = Blueprint('outpatient', __name__)
from .import views