#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES -------
import datetime
import decimal
import sendgrid
from sqlalchemy import desc
from sqlalchemy import or_, and_
from flask import request, render_template, flash, current_app, redirect, abort, jsonify, url_for
from forms import *
from time import time
from flask_login import login_required, current_user

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app, logger
from . import addresses_page
from models import Address
from app.helpers import *
from app.modules.localization.controllers import get_locale, get_timezone

from app.modules.users.models import User
from app.modules.items.models import Item

# -------  ROUTINGS AND METHODS  -------


# All addresses
@addresses_page.route('/')
@addresses_page.route('/<int:page>')
def index(page=1):
    try:

        users = User.query.filter(User.is_active == True).all()
        guests = users
        items = Address.query.filter(Item.is_active == True).all()


        m_addresses = Address()
        list_addresses = m_addresses.all_data(page, app.config['LISTINGS_PER_PAGE'])


        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = [{'id' : d.id, 'title_en_US' : d.title_en_US, 'description_en_US' : d.description_en_US, 'title_fr_FR' : d.title_fr_FR, 'description_fr_FR' : d.description_fr_FR} for d in list_addresses.items])
        else:
            return render_template("addresses/index.html", items = items, users = users, guests = guests, list_addresses=list_addresses, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        #abort(404)


# Show address
@addresses_page.route('/<int:id>/show', methods=['GET','POST'])
def show(id=1):
    try:
        m_addresses = Address()
        m_address = m_addresses.read_data(id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = m_address)
        else:
            return render_template("addresses/show.html", address=m_address, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# New address
@addresses_page.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    try :

        users = User.query.filter(User.is_active == True).all()
        guests = users

        items = Item.query.filter(Item.is_active == True).all()

        form = Form_Record_Add(request.form)

        if request.method == 'POST':
            if form.validate():
                addresses = Address()

                sanitize_form = {

                    'type' : form.type.data,

                    'title_en_US' : form.title_en_US.data,
                    'title_fr_FR' : form.title_fr_FR.data,

                    'address_line1' : form.address_line1.data,
                    'address_line2' : form.address_line2.data,
                    'city' : form.city.data,
                    'postal_code' : form.postal_code.data,
                    'state_region' : form.state_region.data,
                    'country' : form.country.data,
                    'country_code' : form.country_code.data,
                    'time_zone' : form.time_zone.data,

                    'latitude' : decimal.Decimal(form.latitude.data),
                    'longitude' : decimal.Decimal(form.longitude.data),

                    'amount' : decimal.Decimal(form.amount.data),

                    'user' : form.user.data,

                    'item' : form.item.data,

                    'guests' : form.guests.data,

                    'status' : form.status.data,

                    'is_active' : form.is_active.data

                }

                addresses.create_data(sanitize_form)
                logger.info("Adding a new record.")

                if request.is_xhr == True:
                    return jsonify(data = { message :"Record added successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else :
                    flash("Record added successfully.", category="success")
                    return redirect("/addresses")

        form.action = url_for('addresses_page.new')


        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("addresses/edit.html", form=form, items=items, users = users, guests = guests, title_en_US='New', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# Edit address
@addresses_page.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id=1):
    try :

        # check_admin()

        # users = User.query.all()
        users = User.query.filter(User.is_active == True).all()
        guests = users
        items = Item.query.filter(Item.is_active == True).all()

        addresses = Address()
        address = Address.query.get_or_404(id)

        form = Form_Record_Add(request.form)

        if request.method == 'POST':
            if form.validate():

                sanitize_form = {
                    'type' : form.type.data,

                    'title_en_US' : form.title_en_US.data,
                    'title_fr_FR' : form.title_fr_FR.data,

                    'address_line1' : form.address_line1.data,
                    'address_line2' : form.address_line2.data,
                    'city' : form.city.data,
                    'postal_code' : form.postal_code.data,
                    'state_region' : form.state_region.data,
                    'country' : form.country.data,
                    'country_code' : form.country_code.data,
                    'time_zone' : form.time_zone.data,

                    'latitude' : decimal.Decimal(form.latitude.data),
                    'longitude' : decimal.Decimal(form.longitude.data),

                    'amount' : decimal.Decimal(form.amount.data),

                    'user' : form.user.data,

                    'item' : form.item.data,

                    'guests' : form.guests.data,

                    'status' : form.status.data,

                    'is_active' : form.is_active.data

                }

                addresses.update_data(address.id, sanitize_form)
                logger.info("Editing a new record.")

                if request.is_xhr == True:
                    return jsonify(data = { message :"Record updated successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else :
                    flash("Record updated successfully.", category="success")
                    return redirect("/addresses")

        form.action = url_for('addresses_page.edit', id = address.id)

        form.type.data = address.type

        form.title_en_US.data = address.title_en_US
        form.title_fr_FR.data = address.title_fr_FR

        form.address_line1.data = address.address_line1
        form.address_line2.data = address.address_line2
        form.city.data = address.city
        form.postal_code.data = address.postal_code
        form.state_region.data = address.state_region
        form.country.data = address.country
        form.country_code.data = address.country_code
        form.time_zone.data = address.time_zone

        form.latitude.data = address.latitude
        form.longitude.data = address.longitude


        form.amount.data = address.amount

        if  address.user :
            form.user.data = address.user.id

        if  address.item :
            form.item.data = address.item.id

        if  address.guests :
            form.guests.data = address.guests
        
        

        form.status.data = address.status

        form.is_active.data = address.is_active

        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("addresses/edit.html", form=form, items = items, users = users, guests = guests, title_en_US='Edit', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)



# Delete address
@addresses_page.route('/<int:id>/destroy')
@login_required
def destroy(id=1):
    try:
        addresses = Address()
        address = addresses.query.get_or_404(id)
        addresses.destroy_data(address.id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = {message:"Record deleted successfully.", address : m_address})
        else:
            flash("Record deleted successfully.", category="success")
            return redirect(url_for('addresses_page.index'))

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)