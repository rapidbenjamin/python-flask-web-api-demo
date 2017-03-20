#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import sendgrid
from flask import request, render_template, flash, current_app, jsonify
from time import time

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app, logger
from . import db



# ----- UTILS. Delete them if you don't plan to use them -----

@app.before_first_request
def before_first_request():
    logger.info("-------------------- initializing everything ---------------------")
    db.create_all()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', post = {'title' : 'Error 404' , 'description' : str(e.message) }, app = app ), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

