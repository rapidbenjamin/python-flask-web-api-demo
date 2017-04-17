#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import datetime
import sendgrid
import os
import json
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from flask import request, render_template, flash, current_app, redirect, abort, jsonify, url_for
from forms import *
from time import time
from flask_login import login_required, current_user
from PIL import Image

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app, logger
from . import orders_page
from models import Order
from app.modules.users.models import User
from app.helpers import *
from app.modules.localization.controllers import get_locale, get_timezone
from app import config_name
from constants import *

from app.modules.items.models import Item, OrderItem





# -------  ROUTINGS AND METHODS  ------- 


# All orders
@orders_page.route('/')
@orders_page.route('/<int:page>')
def index(page=1):
    try:
        m_orders = Order()
        list_orders = m_orders.all_data(page, app.config['LISTINGS_PER_PAGE'])
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = [{'id' : d.id, 'title_en_US' : d.title_en_US, 'description_en_US' : d.description_en_US, 'title_fr_FR' : d.title_fr_FR, 'description_fr_FR' : d.description_fr_FR} for d in list_orders.items])
        else:
            return render_template("orders/index.html", list_orders=list_orders, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        #abort(404)






# Show order
@orders_page.route('/<int:id>/show')
def show(id=1):
    try:
        m_orders = Order()
        m_order = m_orders.read_data(id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = m_order)
        else:
            return render_template("orders/show.html", order=m_order, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# New order
@orders_page.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    try :

        form = Form_Record_Add(request.form)

        users = User.query.filter(User.is_active == True).all()
        items = Item.query.filter(Item.is_active == True).all()

        if request.method == 'POST':

            if form.validate():

                orders = Order()

                sanitize_form = {

                    'status' : form.status.data,

                    'user' : form.user.data,

                    'items' : form.items.data,

                    'is_active' : form.is_active.data,
                    'created_at' : form.created_at.data
                }

                orders.create_data(sanitize_form)
                logger.info("Adding a new record.")
                
                if request.is_xhr == True:
                    return jsonify(data = { message :"Record added successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record added successfully.", category="success")
                    return redirect("/orders")

        form.action = url_for('orders_page.new')
        # form.created_at.data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        form.created_at.data = datetime.now().strftime('%Y-%m-%d')

         # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("orders/edit.html", form=form,  users = users, items = items, title_en_US='New', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# Edit order
@orders_page.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id=1):
    try : 

        # check_admin()

        orders = Order()
        order = orders.query.get_or_404(id)

        # users = User.query.all()
        users = User.query.filter(User.is_active == True).all()

        items = Item.query.filter(Item.is_active == True).all()

        # request.form only contains form input data. request.files contains file upload data. 
        # You need to pass the combination of both to the form. 
        form = Form_Record_Add(CombinedMultiDict((request.files, request.form)))

        if request.method == 'POST':
            if form.validate():

                sanitize_form = {

                    'status' : form.status.data,

                    'user' : form.user.data,

                    'items' : form.items.data,

                    'is_active' : form.is_active.data,
                    'created_at' : form.created_at.data
                }

                orders.update_data(order.id, sanitize_form)
                logger.info("Editing a new record.")
                
                if request.is_xhr == True:
                    return jsonify(data = { message :"Record updated successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record updated successfully.", category="success")
                    return redirect("/orders")

        form.action = url_for('orders_page.edit', id = order.id)

        form.status.data = order.status

        if  order.user :
            form.user.data = order.user.id

        if  order.items :
            form.items.data = order.items

        form.is_active.data = order.is_active
        form.created_at.data = string_timestamp_utc_to_string_datetime_utc(order.created_at, '%Y-%m-%d')

        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("orders/edit.html", form=form, users = users, items = items, title_en_US='Edit', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)



# Delete order
@orders_page.route('/<int:id>/destroy')
@login_required
def destroy(id=1):
    try:
        orders = Order()
        order = orders.query.get_or_404(id)

        orders.destroy_data(order.id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = {message:"Record deleted successfully.", order : m_order})
        else:
            flash("Record deleted successfully.", category="success")
            return redirect(url_for('orders_page.index'))

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)