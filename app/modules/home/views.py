#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
from flask import request, render_template, flash, current_app, redirect, abort, jsonify
import sendgrid
from flask_login import login_required, current_user

# ------- IMPORT LOCAL DEPENDENCIES  -------
from . import home_page
from app import app


# HOME PAGE
@app.route('/')
@home_page.route('/')
def index():
    try:
        post = { 'title' : 'Flask api demo' , 'description' : 'Web api ' }

        # html or Json response
        if request.is_xhr == True :
            return jsonify(data = post), 200, {'Content-Type': 'application/json'}
        else:
            return render_template('home/home.html', post = post, app = app )

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        return render_template('404.html', post = {'title' : 'Error' , 'description' : str(ex.message) }, app = app )
        #abort(404)
