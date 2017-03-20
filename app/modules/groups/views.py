#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import sendgrid
from flask import request, render_template, flash, current_app, redirect, abort, jsonify
from forms import *
from time import time

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app, logger
from . import groups_page
from models import Groups


# -------  ROUTINGS AND METHODS  ------- 

# All groups
@groups_page.route('/')
@groups_page.route('/<int:page>')
def groups(page=1):
    try:
        m_groups = Groups()
        list_groups = m_groups.list_all(page, app.config['LISTINGS_PER_PAGE'])
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = [{'id' : d.id, 'title' : d.title, 'description' : d.description} for d in list_groups.items])
        else:
            return render_template("groups/index.html", list_groups=list_groups, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------" + str(ex.message))
        #abort(404)



    

# Show group
@groups_page.route('/show/<int:id>')
def show(id=1):
    try:
        m_groups = Groups()
        m_group = m_groups.get_id(id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = m_group)
        else:
            return render_template("groups/show.html", group=m_group, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------" + str(ex.message))
        abort(404)


# New group
@groups_page.route('/new', methods=['GET', 'POST'])
def new():
    try : 
        form = Form_Record_Add(request.form)

        if request.method == 'POST':
            if form.validate():
                new_record = Groups()

                title = form.title.data
                description = form.description.data

                new_record.add_data(title, description)
                logger.info("Adding a new record.")
                flash("Record added successfully.", category="success")
                return redirect("/groups")

        
         # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form)
        else:
            return render_template("groups/new.html", form=form, app = app)
    except Exception, ex:
        print("------------ ERROR  ------------" + str(ex.message))
        abort(404)






