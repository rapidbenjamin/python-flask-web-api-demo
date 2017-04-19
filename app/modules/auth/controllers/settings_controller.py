#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
from flask import request, render_template, flash, current_app, redirect, abort, jsonify, url_for, session
from flask_login import login_required, login_user, logout_user, current_user
import datetime
from time import time

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app.modules.auth import auth_page
from app import app, logger
from app.modules.auth.forms.settings_form import Form_Record_Settings
from app import db
from app.modules.users.models import User
from app.helpers import *
from app.modules.localization.controllers import get_locale, get_timezone

from app.modules.sections.models import Section, UserSection

# ADMIN SETTINGS PAGE

# Edit user settings
@auth_page.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    try : 

        # check_admin()

        # sections = Section.query.all()
        sections = Section.query.filter(Section.is_active == True).all()
        user = current_user
        
        form = Form_Record_Settings(request.form)

        if request.method == 'POST':
            if form.validate():

                sanitize_form = {
                    'email' : form.email.data,
                    'username' : form.username.data,
                    'sections' : form.sections.data,
                    'is_active' : form.is_active.data
                }

                user.update_data(user.id, sanitize_form)
                logger.info("Editing a new record.")
                
                if request.is_xhr == True:
                    return jsonify(data = { message :"Record updated successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record updated successfully.", category="success")
                    return redirect(url_for('auth_page.profile'))

        
        form.action = url_for('auth_page.settings')
        form.email.data = user.email
        form.username.data = user.username

        if  user.sections :
            form.sections.data = user.sections

        form.is_active.data = user.is_active

        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("auth/settings.html", form=form, sections = sections, title_en_US='Edit', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)