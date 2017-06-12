#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
from flask import request, render_template, flash, current_app, redirect, abort, jsonify, url_for, session
from flask_login import login_required, login_user, logout_user, current_user

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app.modules.auth import auth_page
from app import app
from app.modules.auth.forms.login_form import LoginForm
from app import db
from app.modules.users.models import User
from app.modules.sections.models import Section
from app.helpers import *

# ADMIN PROFILE PAGE

@auth_page.route('/profile')
@login_required
def profile():
    try:
        m_users = User()
        m_user = current_user
        # html or Json response
        if request_wants_json():
            return jsonify(data = m_user)
        else:
            return render_template("users/show.html", user=m_user, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)