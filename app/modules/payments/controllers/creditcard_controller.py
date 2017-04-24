#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import datetime
import sendgrid
import os
import json
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from flask import request, render_template, flash, current_app, g, redirect, abort, jsonify, url_for, session
from forms import *
from time import time
from flask_login import login_required, current_user

import paypalrestsdk as paypal
from paypalrestsdk import *

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app, logger
from app.modules.payments import creditcards_page
from app.modules.payments.models.creditcard_model import Creditcard
from app.modules.users.models import User
from app.helpers import *
from app.modules.localization.controllers import get_locale, get_timezone
from app import config_name
from constants import *

from app.modules.orders.models import Order
from app.modules.payments.models.payment_model import Payment




# -------  ROUTINGS AND METHODS  ------- 

# Encrypt secret data
encrypTool = EncryptTool()

# All creditcards
@creditcards_page.route('/')
@creditcards_page.route('/<int:page>')
def index(page=1):
    try:
        m_creditcards = Creditcard()
        list_creditcards = m_creditcards.all_data(page, app.config['LISTINGS_PER_PAGE'])
        
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = [{'id' : d.id, 'title_en_US' : d.title_en_US, 'description_en_US' : d.description_en_US, 'title_fr_FR' : d.title_fr_FR, 'description_fr_FR' : d.description_fr_FR} for d in list_creditcards.items])
        else:
            return render_template("creditcards/index.html", list_creditcards=list_creditcards, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        #abort(404)




# Show creditcard
@creditcards_page.route('/<int:id>/show')
def show(id=1):
    try:
        m_creditcards = Creditcard()
        m_creditcard = m_creditcards.read_data(id)

        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = m_creditcard)
        else:
            return render_template("creditcards/show.html", creditcard=m_creditcard, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# New creditcard
@creditcards_page.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    try :

        form = Form_Record_Add(request.form)

        users = User.query.filter(User.is_active == True).all()

        if request.method == 'POST':

            if form.validate():

                payments = Creditcard()

                sanitize_form = {

                    'status' : form.status.data,

                    'key_id' : form.key_id.data,

                    'user' : form.user.data,

                    'type' : form.type.data,
                    'encrypted_number'  : encrypTool.to_encrypt(form.encrypted_number.data),
                    'expire_month'  : form.expire_month.data,
                    'expire_year'  : form.expire_year.data,
                    'first_name'  : form.first_name.data,
                    'last_name'  : form.last_name.data,


                    'params' : form.params.data,

                    'comments' : form.comments.data,

                    'is_active' : form.is_active.data
                }

                creditcards.create_data(sanitize_form)
                logger.info("Adding a new record.")
                
                if request.is_xhr == True:
                    return jsonify(data = { message :"Record added successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record added successfully.", category="success")
                    return redirect("/creditcards")

        form.action = url_for('creditcards_page.new')

         # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("creditcards/edit.html", form=form,  users = users, title_en_US='New', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# Edit creditcard
@creditcards_page.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id=1):
    try : 

        # check_admin()

        creditcards = Creditcard()
        creditcard = creditcards.query.get_or_404(id)

        # users = User.query.all()
        users = User.query.filter(User.is_active == True).all()
        orders = Order.query.filter(Order.is_active == True).all()
        creditcards = Creditcard.query.filter(Creditcard.is_active == True).all()

        # request.form only contains form input data. request.files contains file upload data. 
        # You need to pass the combination of both to the form. 
        form = Form_Record_Add(request.form)

        if request.method == 'POST':
            if form.validate():

                sanitize_form = {

                    'status' : form.status.data,

                    'key_id' : form.key_id.data,

                    'user' : form.user.data,

                    'type' : form.type.data,
                    'encrypted_number'  : encrypTool.to_encrypt(form.encrypted_number.data),
                    'expire_month'  : form.expire_month.data,
                    'expire_year'  : form.expire_year.data,
                    'first_name'  : form.first_name.data,
                    'last_name'  : form.last_name.data,

                    'params' : form.params.data,

                    'comments' : form.comments.data,

                    'is_active' : form.is_active.data
                }

                creditcards.update_data(creditcard.id, sanitize_form)

                # Remove current creditcard
                #if creditcard.status != 'cart' and session.get('creditcard_id'):
                    #session.pop('creditcard_id')

                logger.info("Editing a new record.")
                
                if request.is_xhr == True:
                    return jsonify(data = { message :"Record updated successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record updated successfully.", category="success")
                    return redirect("/creditcards")

        form.action = url_for('creditcards_page.edit', id = creditcard.id)

        form.status.data = creditcard.status

        form.key_id.data = creditcard.key_id

        if  creditcard.user :
            form.user.data = creditcard.user.id

        form.type.data = creditcard.type
        form.encrypted_number.data = encrypTool.to_decrypt(creditcard.encrypted_number)
        form.expire_month.data = creditcard.expire_month
        form.expire_year.data = creditcard.expire_year
        form.first_name.data = creditcard.first_name
        form.last_name.data = creditcard.last_name
        
        form.params.data = creditcard.params
        form.comments.data = creditcard.comments

        form.is_active.data = creditcard.is_active

        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("creditcards/edit.html", form=form, users = users, title_en_US='Edit', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)



# Delete creditcard
@creditcards_page.route('/<int:id>/destroy')
@login_required
def destroy(id=1):
    try:
        creditcards = Creditcard()
        creditcard = creditcards.query.get_or_404(id)

        creditcards.destroy_data(creditcard.id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = {message:"Record deleted successfully.", creditcard : m_creditcard})
        else:
            flash("Record deleted successfully.", category="success")
            return redirect(url_for('creditcards_page.index'))

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)