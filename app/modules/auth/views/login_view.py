#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
from flask import request, render_template, flash, current_app, redirect, abort, jsonify, url_for
from flask_login import login_required, login_user, logout_user

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app.modules.auth import auth_page
from app import app
from app.modules.auth.forms.login_form import LoginForm
from app import db
from app.modules.users.models import Users



# AUTHENTICATION PAGE
@auth_page.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an user in through the login form
    """

    form = LoginForm()

    if form.validate_on_submit():
        # check whether user exists in the database and whether
        # the password entered matches the password in the database
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # log user in
            login_user(user)

            # redirect to the dashboard page after login
            if request.is_xhr == True :
                return jsonify(data = user), 200, {'Content-Type': 'application/json'}
            else:
                # redirect to the appropriate page
                if user.is_admin:
                    return redirect(url_for('home_page.dashboard'))
                else:
                    return redirect(url_for('home_page.home'))


        # when login details are incorrect
        else:
            if request.is_xhr == True :
                return jsonify(data =  {message:"Unauthorized : Invalid email or password", user : user}), 422, {'Content-Type': 'application/json'}
            else:
                flash('Unauthorized : Invalid email or password.', category="danger")


    # load login template
    if request.is_xhr == True :
        return jsonify(data = form), 200, {'Content-Type': 'application/json'}
    else:
        return render_template('auth/login.html', form=form, title='Login', app = app)



