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
from app.modules.users.models import Users



# AUTHENTICATION PAGE
@auth_page.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an user in through the login form
    """
    # Check if classic user session already exist
    if session.get('email') and request.is_xhr == True :
            flash('Your are already logged in.', 'info')
            return redirect(url_for('home_page.index'))
    # Check if flask-login user session already exist
    if current_user.is_authenticated and request.is_xhr == False:
        return jsonify(data =  {message:"Your are already logged in."}), 200, {'Content-Type': 'application/json'}

    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        # check whether user exists in the database and whether
        # the password entered matches the password in the database
        user = Users.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            

            # redirect to the dashboard page after login
            if request.is_xhr == True :
                # populate classic session with user  email
                session['email'] = user.email
                return jsonify(data = user), 200, {'Content-Type': 'application/json'}
            else:
                
                # populate flask-login session with user
                login_user(user)

                # redirect to the appropriate page
                if user.is_admin:
                    return redirect(url_for('auth_page.dashboard'))
                else:
                    return redirect(url_for('home_page.index'))


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





