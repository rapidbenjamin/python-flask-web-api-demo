#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import datetime
import sendgrid
from flask import request, render_template, flash, current_app, redirect, abort, jsonify, url_for
from forms import *
from time import time
from flask_login import login_required, current_user

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app, logger
from . import units_page
from models import Units
from app.helpers import *
from app.localization import get_locale, get_timezone

# -------  ROUTINGS AND METHODS  ------- 


# All units
@units_page.route('/')
@units_page.route('/<int:page>')
def units(page=1):
    try:
        m_units = Units()
        list_units = m_units.all_data(page, app.config['LISTINGS_PER_PAGE'])
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = [{'id' : d.id, 'title_en_US' : d.title_en_US, 'description_en_US' : d.description_en_US, 'title_fr_FR' : d.title_fr_FR, 'description_fr_FR' : d.description_fr_FR} for d in list_units.items])
        else:
            return render_template("units/index.html", list_units=list_units, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        #abort(404)



    

# Show unit
@units_page.route('/show/<int:id>')
def show(id=1):
    try:
        m_units = Units()
        m_unit = m_units.read_data(id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = m_unit)
        else:
            return render_template("units/show.html", unit=m_unit, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# New unit
@units_page.route('/new', methods=['GET', 'POST'])
def new():
    try :

        form = Form_Record_Add(request.form)

        if request.method == 'POST':
            if form.validate():
                units = Units()

                sanitize_form = {

                    'slug' : form.slug.data,

                    'title_en_US' : form.title_en_US.data,
                    'title_fr_FR' : form.title_fr_FR.data,

                    'description_en_US' : form.description_en_US.data,
                    'description_fr_FR' : form.description_fr_FR.data,

                    'is_active' : form.is_active.data,
                    'created_at' : form.created_at.data
                }

                units.create_data(sanitize_form)
                logger.info("Adding a new record.")
                
                if request.is_xhr == True:
                    return jsonify(data = { message :"Record added successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record added successfully.", category="success")
                    return redirect("/units")

        form.action = url_for('units_page.new')
        form.created_at.data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

         # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("units/edit.html", form=form,  title='New', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# Edit unit
@units_page.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id=1):
    try : 

        # check_admin()

        units = Units()
        unit = units.query.get_or_404(id)

        form = Form_Record_Add(request.form)

        if request.method == 'POST':
            if form.validate():

                sanitize_form = {
                    'slug' : form.slug.data,

                    'title_en_US' : form.title_en_US.data,
                    'title_fr_FR' : form.title_fr_FR.data,

                    'description_en_US' : form.description_en_US.data,
                    'description_fr_FR' : form.description_fr_FR.data,

                    'is_active' : form.is_active.data,
                    'created_at' : form.created_at.data
                }

                units.update_data(unit.id, sanitize_form)
                logger.info("Editing a new record.")
                
                if request.is_xhr == True:
                    return jsonify(data = { message :"Record updated successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record updated successfully.", category="success")
                    return redirect("/units")

        form.action = url_for('units_page.edit', id = unit.id)

        form.slug.data = unit.slug

        form.title_en_US.data = unit.title_en_US
        form.title_fr_FR.data = unit.title_fr_FR

        form.description_en_US.data = unit.description_en_US
        form.description_fr_FR.data = unit.description_fr_FR

        form.is_active.data = unit.is_active
        form.created_at.data = string_timestamp_utc_to_string_datetime_utc(unit.created_at, '%Y-%m-%d')

        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("units/edit.html", form=form, title='Edit', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)



# Delete unit
@units_page.route('/delete/<int:id>')
def delete(id=1):
    try:
        units = Units()
        unit = units.query.get_or_404(id)
        units.delete_data(unit.id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = {message:"Record deleted successfully.", unit : m_unit})
        else:
            flash("Record deleted successfully.", category="success")
            return redirect(url_for('units_page.units'))

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)