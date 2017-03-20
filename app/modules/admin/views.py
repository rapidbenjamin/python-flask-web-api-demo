#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
from flask import request, render_template, flash, current_app, redirect, abort, jsonify
import sendgrid

# ------- IMPORT LOCAL DEPENDENCIES  -------
from . import admin_page
from app import app


# ADMIN PAGE
@admin_page.route('/')
def index():
    try:
        post = { 'title' : 'Admin' , 'description' : 'management ' }

        # html or Json response
        if request.is_xhr == True :
            return jsonify(data = post)
        else:
            return render_template('admin/admin.html', post = post, app = app )

    except Exception, ex:
        print("------------ ERROR  ------------" + str(ex.message))
        return render_template('404.html', post = {'title' : 'Error' , 'description' : str(ex.message) }, app = app )
        #abort(404)