#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
from flask import request, render_template, flash, current_app, redirect, abort, jsonify
import sendgrid

# ------- IMPORT LOCAL DEPENDENCIES  -------
from ... import db
from . import articles_page
from app import app
from app.helpers import threaded_async

# -------  ROUTINGS AND METHODS  -------
# ARTICLES
@articles_page.route('/')
@articles_page.route('/<article>')
def show(article = 'article', post = { 'id': '0', 'title' : 'Default title' , 'description' : 'default Description' }):
    try:
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = post), 200, {'Content-Type': 'application/json'}
        else:
            return render_template('articles/%s.html' % article, post = post, app = app )

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        return render_template('articles/default.html', post = {'id': '0', 'title' : 'Error' , 'description' : str(ex.message) }, app = app )
        #abort(404)




