#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import sendgrid
from flask import request, render_template, flash, current_app, jsonify, abort, g, request, session, redirect, url_for
from time import time
from flask_wtf.csrf import CSRFError
from flask_login import login_required, login_user, logout_user, current_user
import json
from dateutil import *
from dateutil import tz
# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app, logger
from . import db
from app.modules.localization.controllers import *
from app.modules.localization import localization_service, babel








# ----- UTILS. Delete them if you don't plan to use them -----



# ------- START DATABASE  -------
@app.before_first_request
def before_first_request():
    logger.info("-------------------- initializing DB ---------------------\n")
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.create_all()
        # and/or populate (not working db.cursor() error)
        # init_db()


def init_db():
    """Initializes the database."""
    with app.open_resource('../data/schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

"""
@app.teardown_appcontext
def close_db(error):
    \"""Closes the database again at the end of the request.\"""
    db.close()
"""
# ----- EN DATABASE -----



# ----- BASIC REQUESTS -----

# CHANGE THEME
@app.before_request
def before_request():
    if request.args and 'theme' in request.args:
        app.config['BOOTSWATCH_THEME'] = request.args['theme']
        print("********************** \n\n THEME CHANGE : " + request.args['theme'] + "\n\n ***************************\n\n")


# Maintenance - Coming soon page
@app.route('/maintenance')
def maintenance():
    g.current_lang = app.config['BABEL_DEFAULT_LOCALE']
    g.current_timezone = app.config['BABEL_DEFAULT_TIMEZONE']
    return render_template('maintenance.html', post = {'title_en_US' : 'Coming soon' , 'description_en_US' : 'maintenance page' },  app = app )


# Flash messages notifications collection
@app.route('/flash')
def flash_notify():
    g.current_lang = app.config['BABEL_DEFAULT_LOCALE']
    g.current_timezone = app.config['BABEL_DEFAULT_TIMEZONE']

    flash("Flash success: Message notification service", category="success")
    flash("Flash info : Message notification service", category="info")
    flash("Flash warning : Message notification service", category="warning")
    flash("Flash error: Message notification service", category="danger")

    return render_template('flash.html', post = {'title_en_US' : 'Flash messages' , 'description_en_US' : 'flash collection page' },  app = app )




@app.errorhandler(403)
def page_forbidden(e):
    g.current_lang = app.config['BABEL_DEFAULT_LOCALE']
    g.current_timezone = app.config['BABEL_DEFAULT_TIMEZONE']
    return render_template('403.html', post = {'title_en_US' : 'Error 403' , 'description_en_US' : str(e.description) },  app = app ), 403


@app.errorhandler(404)
def page_not_found(e):
    g.current_lang = app.config['BABEL_DEFAULT_LOCALE']
    g.current_timezone = app.config['BABEL_DEFAULT_TIMEZONE']
    return render_template('404.html', post = {'title_en_US' : 'Error 404' , 'description_en_US' : str(e.message) },  app = app ), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


# handle CSRF form protection error 
# Invalid CSRF Token
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    g.current_lang = app.config['BABEL_DEFAULT_LOCALE']
    g.current_timezone = app.config['BABEL_DEFAULT_TIMEZONE']
    return render_template('403.html', post = {'title_en_US' : 'Error CSRF form protection 403' , 'description_en_US' : str(e.description) },  app = app ), 403


@app.errorhandler(400)
def bad_request(e):
    g.current_lang = app.config['BABEL_DEFAULT_LOCALE']
    g.current_timezone = app.config['BABEL_DEFAULT_TIMEZONE']
    return render_template('400.html', post = {'title_en_US' : 'Error 400 Bad request' , 'description_en_US' : str(e.description) },  app = app ), 400


@app.errorhandler(422)
def unprocessable(e):
    g.current_lang = app.config['BABEL_DEFAULT_LOCALE']
    g.current_timezone = app.config['BABEL_DEFAULT_TIMEZONE']
    return render_template('422.html', post = {'title_en_US' : 'Unprocessable Entity' , 'description_en_US' : str(e.description) },  app = app ), 422



@app.route('/404')
def error_404():
    abort(404)

@app.route('/500')
def error():
    abort(500)




