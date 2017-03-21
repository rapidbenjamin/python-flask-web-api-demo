#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import sendgrid
from flask import request, render_template, flash, current_app, redirect, abort, jsonify, url_for
from forms import *
from time import time

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app, logger
from . import groups_page
from models import Groups


# -------  ROUTINGS AND METHODS  ------- 


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

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
        print("------------ ERROR  ------------\n" + str(ex.message))
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
        print("------------ ERROR  ------------\n" + str(ex.message))
        abort(404)


# New group
@groups_page.route('/new', methods=['GET', 'POST'])
def new():
    try : 

        # check_admin()

        form = Form_Record_Add(request.form)

        if request.method == 'POST':
            if form.validate():
                groups = Groups()

                sanitize_form = {
                    'title' : form.title.data,
                    'description' : form.description.data
                }

                groups.add_data(sanitize_form)
                logger.info("Adding a new record.")
                
                if request.is_xhr == True:
                    return jsonify(data = { message :"Record added successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record added successfully.", category="success")
                    return redirect("/groups")

        
         # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("groups/new.html", form=form, app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        abort(404)


# Edit group
@groups_page.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id=1):
    try : 

        # check_admin()

        groups = Groups()
        group = groups.query.get_or_404(id)

        form = Form_Record_Add(request.form)

        if request.method == 'POST':
            if form.validate():

                sanitize_form = {
                    'title' : form.title.data,
                    'description' : form.description.data
                }

                groups.update_data(group.id, sanitize_form)
                logger.info("Editing a new record.")
                
                if request.is_xhr == True:
                    return jsonify(data = { message :"Record updated successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record updated successfully.", category="success")
                    return redirect("/groups")

        form.title.data = group.title
        form.description.data = group.description
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("groups/new.html", form=form, app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        abort(404)



# Delete group
@groups_page.route('/delete/<int:id>')
def delete(id=1):
    try:
        groups = Groups()
        group = groups.query.get_or_404(id)
        groups.delete_data(group.id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = {message:"Record deleted successfully.", group : m_group})
        else:
            flash("Record deleted successfully.", category="success")
            return redirect(url_for('groups_page.groups'))

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        abort(404)