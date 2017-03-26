#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import sendgrid
from flask import request, render_template, flash, current_app, redirect, abort, jsonify, url_for
from forms import *
from time import time

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app, logger
from . import users_page
from models import Users
from app.modules.groups.models import Groups


# -------  ROUTINGS AND METHODS  ------- 

# All users
@users_page.route('/')
@users_page.route('/<int:page>')
def users(page=1):
    try:
        m_users = Users()
        list_users = m_users.list_all(page, app.config['LISTINGS_PER_PAGE'])
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = [{'id' : d.id, 'email' : d.email, 'username' : d.username} for d in list_users.items])
        else:
            return render_template("users/index.html", list_users=list_users, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        #abort(404)



    

# Show user
@users_page.route('/show/<int:id>')
def show(id=1):
    try:
        m_users = Users()
        m_user = m_users.get_user(id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = m_user)
        else:
            return render_template("users/show.html", user=m_user, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# New user
@users_page.route('/new', methods=['GET', 'POST'])
def new():
    try : 
        form = Form_Record_Add(request.form)
        groups = Groups.query.all()

        if request.method == 'POST':
            if form.validate():
                users = Users()

                sanitize_form = {
                    'email' : form.email.data,
                    'username' : form.username.data,
                    'group' : form.group.data
                }                

                users.add_data(sanitize_form)
                logger.info("Adding a new record.")
                if request.is_xhr == True:
                    return jsonify(data = { message :"Record added successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record added successfully.", category="success")
                    return redirect("/users")

        form.action = url_for('users_page.new')
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("users/edit.html", form=form, groups = groups, title='New', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)

# Edit user
@users_page.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id=1):
    try : 

        # check_admin()

        groups = Groups.query.all()
        user = Users.query.get_or_404(id)
        
        form = Form_Record_Add(request.form)

        if request.method == 'POST':
            if form.validate():

                group = form.group.data

                sanitize_form = {
                    'email' : form.email.data,
                    'username' : form.username.data,
                    'group' : form.group.data
                }

                user.update_data(user.id, sanitize_form)
                logger.info("Editing a new record.")
                
                if request.is_xhr == True:
                    return jsonify(data = { message :"Record updated successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record updated successfully.", category="success")
                    return redirect("/users")

        
        form.action = url_for('users_page.edit', id = user.id)
        form.email.data = user.email
        form.username.data = user.username
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("users/edit.html", form=form,  groups = groups, title='Edit', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)



# Delete user
@users_page.route('/delete/<int:id>')
def delete(id=1):
    try:
        users = Users()
        user = users.query.get_or_404(id)
        users.delete_data(user.id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = {message:"Record deleted successfully.", user : m_user})
        else:
            flash("Record deleted successfully.", category="success")
            return redirect(url_for('users_page.users'))

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)




