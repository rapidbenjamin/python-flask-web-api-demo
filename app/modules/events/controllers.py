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
from . import events_page
from models import Event
from app.helpers import *
from app.modules.localization.controllers import get_locale, get_timezone

from app.modules.users.models import User
from app.modules.items.models import Item

# -------  ROUTINGS AND METHODS  ------- 


# All events
@events_page.route('/')
@events_page.route('/<int:page>')
def index(page=1):
    try:
        
        users = User.query.filter(User.is_active == True).all()
        items = Event.query.filter(Item.is_active == True).all()


        m_events = Event()
        list_events = m_events.all_data(page, app.config['LISTINGS_PER_PAGE'])

        
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = [{'id' : d.id, 'title_en_US' : d.title_en_US, 'description_en_US' : d.description_en_US, 'title_fr_FR' : d.title_fr_FR, 'description_fr_FR' : d.description_fr_FR} for d in list_events.items])
        else:
            return render_template("events/index.html", items = items, users = users, list_events=list_events, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        #abort(404)


# Show event
@events_page.route('/<int:id>/show', methods=['GET','POST'])
def show(id=1):
    try:
        m_events = Event()
        m_event = m_events.read_data(id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = m_event)
        else:
            return render_template("events/show.html", event=m_event, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# New event
@events_page.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    try :

        users = User.query.filter(User.is_active == True).all()
        items = Item.query.filter(Item.is_active == True).all()
        


        form = Form_Record_Add(request.form)

        if request.method == 'POST':
            if form.validate():
                events = Event()

                sanitize_form = {

                    'type' : form.type.data,

                    'price' : decimal.Decimal(form.price.data),

                    'user' : form.user.data,

                    'item' : form.item.data,

                    'start' : form.start.data,

                    'end' : form.end.data,

                    'days' : form.days.data,

                    'allday' : form.allday.data,

                    'status' : form.status.data,

                    'is_active' : form.is_active.data,

                }

                events.create_data(sanitize_form)
                logger.info("Adding a new record.")
                
                if request.is_xhr == True:
                    return jsonify(data = { message :"Record added successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record added successfully.", category="success")
                    return redirect("/events")

        form.action = url_for('events_page.new')

        # form.start.data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        form.start.data = datetime.now().strftime('%Y-%m-%d')

        # form.end.data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        form.end.data = datetime.now().strftime('%Y-%m-%d')


         # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("events/edit.html", form=form, items=items, users = users, title_en_US='New', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# Edit event
@events_page.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id=1):
    try : 

        # check_admin()

        # users = User.query.all()
        users = User.query.filter(User.is_active == True).all()
        items = Item.query.filter(Item.is_active == True).all()

        events = Event()
        event = Event.query.get_or_404(id)

        form = Form_Record_Add(request.form)

        if request.method == 'POST':
            if form.validate():

                sanitize_form = {
                    'type' : form.type.data,

                    'price' : decimal.Decimal(form.price.data),

                    'user' : form.user.data,

                    'item' : form.item.data,

                    'start' : form.start.data,

                    'end' : form.end.data,

                    'days' : form.days.data,

                    'allday' : form.allday.data,

                    'status' : form.status.data,

                    'is_active' : form.is_active.data,

                }

                events.update_data(event.id, sanitize_form)
                logger.info("Editing a new record.")

                if request.is_xhr == True:
                    return jsonify(data = { message :"Record updated successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else :
                    flash("Record updated successfully.", category="success")
                    return redirect("/events")

        form.action = url_for('events_page.edit', id = event.id)

        form.type.data = event.type

        form.price.data = event.price

        if  event.user :
            form.user.data = event.user.id

        if  event.item :
            form.item.data = event.item.id
        
        # form.start.data = string_timestamp_utc_to_string_datetime_utc(event.start, '%Y-%m-%d %H:%M:%S')
        form.start.data = string_timestamp_utc_to_string_datetime_utc(event.start, '%Y-%m-%d')

        # form.end.data = string_timestamp_utc_to_string_datetime_utc(event.end, '%Y-%m-%d %H:%M:%S')
        form.end.data = string_timestamp_utc_to_string_datetime_utc(event.end, '%Y-%m-%d')

        form.days.data = event.days

        form.allday.data = event.allday

        form.status.data = event.status

        form.is_active.data = event.is_active
        

        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("events/edit.html", form=form, items = items, users = users, title_en_US='Edit', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)



# Delete event
@events_page.route('/<int:id>/destroy')
@login_required
def destroy(id=1):
    try:
        events = Event()
        event = events.query.get_or_404(id)
        events.destroy_data(event.id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = {message:"Record deleted successfully.", event : m_event})
        else:
            flash("Record deleted successfully.", category="success")
            return redirect(url_for('events_page.index'))

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)