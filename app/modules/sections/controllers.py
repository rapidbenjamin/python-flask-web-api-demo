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
from . import sections_page
from models import Section
from app.helpers import *
from app.modules.localization.controllers import get_locale, get_timezone

from app.modules.users.models import User
from app.modules.items.models import Item, SectionItem

# -------  ROUTINGS AND METHODS  ------- 


# All sections
@sections_page.route('/')
@sections_page.route('/<int:page>')
def index(page=1):
    try:
        m_sections = Section()
        list_sections = m_sections.all_data(page, app.config['LISTINGS_PER_PAGE'])
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = [{'id' : d.id, 'title_en_US' : d.title_en_US, 'description_en_US' : d.description_en_US, 'title_fr_FR' : d.title_fr_FR, 'description_fr_FR' : d.description_fr_FR} for d in list_sections.items])
        else:
            return render_template("sections/index.html", list_sections=list_sections, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        #abort(404)


# Show section
@sections_page.route('/<int:id>/show', methods=['GET','POST'])
def show(id=1):
    try:
        m_sections = Section()
        m_section = m_sections.read_data(id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = m_section)
        else:
            return render_template("sections/show.html", section=m_section, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# New section
@sections_page.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    try :
        users = User.query.filter(User.is_active == True).all()
        form = Form_Record_Add(request.form)
        sections = Section.query.filter(Section.is_active == True).all()
        items = Item.query.filter(Item.is_active == True).all()

        if request.method == 'POST':
            if form.validate():
                sections = Section()

                sanitize_form = {

                    'slug' : form.slug.data,

                    'parent' : form.parent.data,

                    'title_en_US' : form.title_en_US.data,
                    'title_fr_FR' : form.title_fr_FR.data,

                    'description_en_US' : form.description_en_US.data,
                    'description_fr_FR' : form.description_fr_FR.data,

                    'users' : form.users.data,

                    'items' : form.items.data,

                    'is_active' : form.is_active.data
                }

                Section().create_data(sanitize_form)
                logger.info("Adding a new record.")
                
                if request.is_xhr == True:
                    return jsonify(data = { message :"Record added successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record added successfully.", category="success")
                    return redirect("/sections")

        form.action = url_for('sections_page.new')

         # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("sections/edit.html", form=form, sections = sections, items = items, users=users,  title_en_US='New', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# Edit section
@sections_page.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id=1):
    try : 

        # check_admin()
        users = User.query.filter(User.is_active == True).all()

        # sections = Section.query.all()
        sections = Section.query.filter(Section.is_active == True).all()

        # items = Item.query.all()
        items = Item.query.filter(Item.is_active == True).all()

        section = Section.query.get_or_404(id)

        form = Form_Record_Add(request.form)

        if request.method == 'POST':
            if form.validate():

                sanitize_form = {
                    'slug' : form.slug.data,

                    'parent' : form.parent.data,

                    'title_en_US' : form.title_en_US.data,
                    'title_fr_FR' : form.title_fr_FR.data,

                    'description_en_US' : form.description_en_US.data,
                    'description_fr_FR' : form.description_fr_FR.data,

                    'users' : form.users.data,

                    'items' : form.items.data,

                    'is_active' : form.is_active.data
                }


                Section().update_data(section.id, sanitize_form)
                logger.info("Editing a new record.")

                if request.is_xhr == True:
                    return jsonify(data = { message :"Record updated successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record updated successfully.", category="success")
                    return redirect("/sections")

        form.action = url_for('sections_page.edit', id = section.id)

        form.slug.data = section.slug

        if  section.parent :
            form.parent.data = section.parent.id

        form.title_en_US.data = section.title_en_US
        form.title_fr_FR.data = section.title_fr_FR

        form.description_en_US.data = section.description_en_US
        form.description_fr_FR.data = section.description_fr_FR


        if  section.users :
            form.users.data = section.users

        if  section.items :
            form.items.data = section.items

        form.is_active.data = section.is_active
        
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("sections/edit.html", form=form, sections = sections, items = items, users=users, title_en_US='Edit', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)



# Delete section
@sections_page.route('/<int:id>/destroy')
@login_required
def destroy(id=1):
    try:
        sections = Section()
        section = sections.query.get_or_404(id)        

        if section.children:
            # html or Json response
            if request.is_xhr == True :
                    return jsonify(data =  {message:"Unauthorized : Must delete child's section' first"}), 422, {'Content-Type': 'application/json'}
            else:
                flash("Unauthorized : Must delete child's section first.", category="danger")
                return redirect(url_for('sections_page.index'))

        else :
            sections.destroy_data(section.id)
            # html or Json response
            if request.is_xhr == True:
                return jsonify(data = {message:"Record deleted successfully.", section : m_section})
            else:
                flash("Record deleted successfully.", category="success")
                return redirect(url_for('sections_page.index'))

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)