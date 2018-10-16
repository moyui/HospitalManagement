from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint

db = SQLAlchemy()
main = Blueprint('main', __name__)
