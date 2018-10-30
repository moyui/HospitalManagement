from flask import render_template, redirect, request, url_for, flash
from . import charges
from .form import PreChargeForm
from .model import InPatientDeposit, InPatientTotalCost
from .. import db

@charges.route('/charges/deposit/<id>', methods=['GET', 'POST'])
def getDeposit(id):
    form = PreChargeForm()
    