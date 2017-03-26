#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
from flask import request, render_template, flash, current_app, redirect, abort, jsonify, url_for, session
from flask_login import login_required, login_user, logout_user, current_user
import base64

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app.modules.auth import auth_page
from app import app
from app.modules.auth.forms.registration_form import RegistrationForm
from app import db
from app.modules.users.models import Users



# AUTHENTICATION PAGE
@auth_page.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an User to the database through the registration form
    """
    try:
        # Check if user session already exist
        if session.get('email') and request.is_xhr == False :
                flash('Your are already logged in.', 'info')
                return redirect(url_for('home_page.index'))

        form = RegistrationForm()
        # Check  if form is submited
        if request.method == 'POST' and form.validate_on_submit():
            
            # Check if username already exist     
            existing_username = Users.query.filter_by(username=form.username.data).first()
            # Check if email already exist
            existing_email = Users.query.filter_by(email=form.email.data).first()

            # Check validations
            if existing_username and existing_email :                
                # redirect to the login page or Json response
                if request.is_xhr == True :
                    return jsonify(data = {message : "This username or email has been already taken. Try another one.", form : form}), 422, {'Content-Type': 'application/json'}
                else:
                    flash('This username has been already taken. Try another one.', 'warning')
                    return render_template('auth/register.html', form=form, title='Register', app = app)

            # Check form errors
            if form.errors :                
                # redirect to the login page or Json response
                if request.is_xhr == True :
                    return jsonify(data = {message : form.errors, form : form}), 422, {'Content-Type': 'application/json'}
                else:
                    flash(form.errors, 'danger')
                    return render_template('auth/register.html', form=form, title='Register', app = app)

            
             # password decoding  when remote app client
            if request.is_xhr == True :
                form.password.data = base64.b64decode(form.password.data).decode('UTF-8')

            # create user
            user = Users(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)
            
            # Save new user to the database
            db.session.add(user)
            db.session.commit()

            # redirect to the login page or Json response
            if request.is_xhr == True :
                return jsonify(data = {message : "You have successfully registered! You may now login", user : user}), 200, {'Content-Type': 'application/json'}
            else:
                flash('You have successfully registered! You may now login.', 'success')
                return redirect(url_for('auth_page.login'))
        # load registration template
        if request.is_xhr == True :
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template('auth/register.html', form=form, title='Register', app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        return render_template('404.html', post = {'title' : 'Error' , 'description' : str(ex.message) }, app = app )
        #abort(404)

