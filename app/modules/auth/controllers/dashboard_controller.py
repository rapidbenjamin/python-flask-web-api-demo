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



# ADMIN DASHBOARD PAGE


def check_is_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not(current_user.is_admin):
        abort(403)

@auth_page.route('/dashboard')
@login_required
def dashboard():
    post = { 'title_en_US' : 'Dashboard' , 'description_en_US' : 'you can customize your stuffs here' }
    # prevent non-admins from accessing the page
    check_is_admin()
    return render_template('auth/dashboard.html', post = post, app = app )
