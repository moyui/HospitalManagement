from .model import UserGroup, AdminTable
from . import main

@main.route('/createadmin', method=['GET', 'POST'])
def createAdmin():
    
