#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import sendgrid
from flask import request, render_template, flash, current_app, redirect, abort, jsonify
from forms import *
from time import time

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app, logger
from . import users_page
from models import Users


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
            return jsonify(data = [{'id' : d.id, 'first_name' : d.first_name, 'last_name' : d.last_name} for d in list_users.items])
        else:
            return render_template("users/index.html", list_users=list_users, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------" + str(ex.message))
        #abort(404)



    

# Show user
@users_page.route('/show/<int:id>')
def show(id=1):
    try:
        m_users = Users()
        m_user = m_users.get_id(id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = m_user)
        else:
            return render_template("users/show.html", user=m_user, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------" + str(ex.message))
        abort(404)


# New user
@users_page.route('/new', methods=['GET', 'POST'])
def new():
    try : 
        form = Form_Record_Add(request.form)

        if request.method == 'POST':
            if form.validate():
                new_record = Users()

                first_name = form.first_name.data
                last_name = form.last_name.data

                new_record.add_data(first_name, last_name)
                logger.info("Adding a new record.")
                flash("Record added successfully.", category="success")
                return redirect("/users")

        
         # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form)
        else:
            return render_template("users/new.html", form=form, app = app)
    except Exception, ex:
        print("------------ ERROR  ------------" + str(ex.message))
        abort(404)






