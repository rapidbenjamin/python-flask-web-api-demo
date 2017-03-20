#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
from flask import request, render_template, flash, current_app, redirect, abort, jsonify
import sendgrid

# ------- IMPORT LOCAL DEPENDENCIES  -------
from . import authentication_page
from app import app


# AUTHENTICATION PAGE
@authentication_page.route('/')
def index():
    try:
        post = { 'title' : 'Authentication' , 'description' : 'Authentication ' }

        # html or Json response
        if request.is_xhr == True :
            return jsonify(data = post)
        else:
            return render_template('authentication/authentication.html', post = post, app = app )

    except Exception, ex:
        print("------------ ERROR  ------------" + str(ex.message))
        return render_template('404.html', post = {'title' : 'Error' , 'description' : str(ex.message) }, app = app )
        #abort(404)