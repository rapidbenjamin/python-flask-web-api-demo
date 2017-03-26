#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import g
from app import db, login_manager
from flask_login import current_user

# ------- IMPORT LOCAL DEPENDENCIES  -------
from . import login_view, register_view, logout_view, dashboard_view
from app.modules.users.models import Users
from app.modules.auth import auth_page




# ----- FLASK LOGIN SPECIAL REQUESTS  -----
@auth_page.before_request
def get_current_user():
    g.user = current_user
    
# Set user_loader callback for session management 
# which Flask-Login uses to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    # return Users.query.filter(Users.id == user_id)
    return Users.query.get(int(user_id))

