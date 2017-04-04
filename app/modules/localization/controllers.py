#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
from flask import g, request, redirect, url_for, session
from dateutil import *
from dateutil import tz
import json

from flask_login import login_required, login_user, logout_user, current_user

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app
from . import localization_service, babel



# SERVICES

@babel.localeselector
def get_locale():
    """Direct babel to use the language defined in the session, the current user or the browser"""
    # the current user can be stored on the flask.g object.See example with flask-login : g.user = current_user

    # FROM USER SWITCH LANGUAGE BUTTON :  when user update current language 
    if request.args and 'lang' in request.args:
        session['current_lang'] = request.args['lang']
        print("********************** \n\n REQUEST ARGS : " + request.args['lang'] + "\n\n ***************************\n\n")
        return request.args['lang']

    # FROM USER SESSION :  from a server-side session current language
    if 'current_lang' in session:
        print("********************** \n\n SESSION : " + session['current_lang'] + "\n\n ***************************\n\n")
        return session['current_lang']    

    # FROM BROWSER HEADER ACCEPT_LANGUAGE:
    # header the browser transmits.  We support de/fr/en in this
    # example.  The best match wins.
    # return request.accept_languages.best_match(['de', 'fr', 'en'])
    browser_lang = request.accept_languages.best_match(app.config['ALLOWED_LANGUAGES'].keys())
    if browser_lang is not None:
        session['current_lang'] = browser_lang
        print("********************** \n\n BROWSER LANG : " + browser_lang + "\n\n ***************************\n\n")
        return browser_lang
    
    # FROM APP DEFAULT CONFIG
    print("********************** \n\n APP CONFIG  : " + app.config['BABEL_DEFAULT_LOCALE'] + "\n\n ***************************\n\n")
    return app.config['BABEL_DEFAULT_LOCALE']
    

@babel.timezoneselector
def get_timezone():
    """Direct babel to use the timezone defined in the session, the current user or the browser"""
    # the current user must be stored on the flask.g object.See example with flask-login : g.user = current_user

    
    # FROM USER SESSION : a server-side session current timezone
    current_timezone = getattr(session, 'current_timezone', None)
    if 'current_timezone' in session :
        return current_timezone


    # FROM USER TIMEZONE DATA : when user is logged in, use the timezone from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        session['current_timezone'] = user.timezone
        return user.timezone
    
    # FROM BROWSER TIMEZONE : auto detect timezone
    browser_tz = tz.tzlocal()
    if browser_tz is not None:
        session['current_timezone'] = browser_tz
        return browser_tz
    
    # FROM APP DEFAULT CONFIG
    session['current_timezone'] = app.config['BABEL_DEFAULT_TIMEZONE']
    return app.config['BABEL_DEFAULT_TIMEZONE']

@app.before_request
def before_request():
    if '/static/' not in request.path:
        if 'current_lang' in session :
            print("********************** \n\n SESSION LANG : " + session['current_lang'] + "\n\n ***************************\n\n")
        
        
        # create app context  current language
        g.current_lang = get_locale()
        print("********************** \n\n G LANG : " + g.current_lang + "\n\n ***************************\n\n")

        # create app context  current language
        g.timezone = get_timezone()
        print("********************** \n\n TIMEZONE : " + str(g.timezone) + "\n\n ***************************\n\n")



