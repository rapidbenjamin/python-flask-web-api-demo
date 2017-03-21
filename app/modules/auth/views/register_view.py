#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
from flask import request, render_template, flash, current_app, redirect, abort, jsonify, url_for
from flask_login import login_required, login_user, logout_user

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

        form = RegistrationForm()
        if form.validate_on_submit():
            user = Users(email=form.email.data,
                                username=form.username.data,
                                first_name=form.first_name.data,
                                last_name=form.last_name.data,
                                password=form.password.data)

            # add user to the database
            db.session.add(user)
            db.session.commit()

            # redirect to the login page or Json response
            if request.is_xhr == True :
                return jsonify(data = {message : "You have successfully registered! You may now login", user : user}), 200, {'Content-Type': 'application/json'}
            else:
                flash('You have successfully registered! You may now login.')
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

