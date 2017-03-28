#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import sendgrid
from flask import request, render_template, flash, current_app, jsonify, abort, g
from time import time

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app, logger, config_name
from . import db
from config import app_config



# ----- UTILS. Delete them if you don't plan to use them -----

@app.before_first_request
def before_first_request():
    logger.info("-------------------- initializing everything ---------------------\n")

    # create global current language
    g.current_lang = app_config[config_name].BABEL_DEFAULT_LOCALE
    g.current_timezone = app_config[config_name].BABEL_DEFAULT_TIMEZONE

    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.create_all()


# ----- BASIC REQUESTS -----
@app.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html', post = {'title' : 'Error 403' , 'description' : 'Forbidden' }, app = app ), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', post = {'title' : 'Error 404' , 'description' : str(e.message) }, app = app ), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.route('/500')
def error():
    abort(500)




