#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
from flask import request, render_template, flash, current_app, redirect, abort, jsonify, url_for, session
from flask_login import login_required, login_user, logout_user, current_user

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app.modules.auth import auth_page
from app import app
from app import db
from app.modules.users.models import User



# AUTHENTICATION PAGE

@auth_page.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an user out through the logout link
    """
    try:
        

        # redirect to the login page
        if request.is_xhr == True :
            # Remove classic session
            if 'email' in session:
                session.pop('email')
                session.pop('current_lang')
                session.pop('order_id')
                session.clear()
            return jsonify(data = {message:"You have successfully been logged out"}), 200, {'Content-Type': 'application/json'}
        else:
            # Remove flask login session
            logout_user()
            session.pop('email')
            session.pop('current_lang')
            session.pop('order_id')
            session.clear()
            flash('You have successfully been logged out', 'info')
            return redirect(url_for('auth_page.login'))


    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        return render_template('404.html', post = {'title_en_US' : 'Error' , 'description_en_US' : str(ex.message) }, app = app )
        #abort(404)