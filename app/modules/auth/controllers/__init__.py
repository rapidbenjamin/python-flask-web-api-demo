#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import g, redirect, request, url_for, flash
from app import db
from flask_login import current_user, logout_user

from flask import session

import base64

# ------- IMPORT LOCAL DEPENDENCIES  -------
from . import login_controller, register_controller, logout_controller, dashboard_controller, profile_controller, settings_controller
from app.modules.users.models import User
from app.modules.auth import auth_page, login_manager
from app.helpers import *



# ----- FLASK LOGIN SPECIAL REQUESTS  -----
@auth_page.before_request
def get_current_user():
    g.user = current_user
    
# Set user_loader callback for session
# which Flask-Login uses to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    # return User.query.filter(User.id == user_id)
    return User.query.get(int(user_id))



# Set user_loader callback for token header
# which Flask-Login uses to reload the user object from the user ID stored in token header
@login_manager.request_loader
def load_user_from_request(request):
    token = request.headers.get('Authorization')
    # first, try to login using the token url arg
    if token is None:
        token = request.args.get('token')

    # next, try to login using Basic Auth
    if token is not None:
        token = token.replace('Basic ', '', 1)
        try:
            token = base64.b64decode(token)
        except TypeError:
            pass
        
        username,password = token.split(":") # naive token

         # password decoding  when remote app client
        if request_wants_json() :
            form.password.data = base64.b64decode(form.password.data).decode('UTF-8')
            
        user = User.query.filter_by(username=username).first()
        if (user is not None):            
            if (user.check_password(password)):
                return user
    # finally, return None if both methods did not login the user
    return None


# Control access management
@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Unauthorized access : You must login or register first | Previous link : ' + request.path, category="warning")
    return redirect(url_for('auth_page.login', next=request.path))







