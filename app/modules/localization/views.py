#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
from flask import g, request
from dateutil import *
from dateutil import tz


# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app
from . import localization_service, babel
from app import config_name


# SERVICES

# @babel.localeselector
def get_locale():
    """Direct babel to use the language defined in the session, the current user or the browser"""
    # the current user can be stored on the flask.g object.See example with flask-login : g.user = current_user

    # you can get it by creating a global current language
    current_lang = getattr(g, 'current_lang', None)
    if current_lang is not None:
        return current_lang

   
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale    

    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support de/fr/en in this
    # example.  The best match wins.

    # return request.accept_languages.best_match(['de', 'fr', 'en'])
    return request.accept_languages.best_match(app.config['ALLOWED_LANGUAGES'].keys())
    

# @babel.timezoneselector
def get_timezone():
    """Direct babel to use the timezone defined in the session, the current user or the browser"""
    # the current user must be stored on the flask.g object.See example with flask-login : g.user = current_user

    # you can get it by creating a global current language
    current_timezone = getattr(g, 'current_timezone', None)
    if current_timezone is not None:
        return current_timezone
    
    # if a user is logged in, use the timezone from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone
    
    # otherwise auto detect timezone
    return  tz.tzlocal()

@app.before_request
def before_request():
    if '/static/' not in request.path:
        # create global current language if not exist
        current_lang = getattr(g, 'current_lang', None)
        if current_lang is None:
            g.current_lang = get_locale()
            current_lang = g.current_lang

        if request.args and 'lang' in request.args:
            g.current_lang = request.args['lang']
            current_lang = g.current_lang

        # create global current timezone if not exist
        current_timezone = getattr(g, 'current_timezone', None)
        if current_timezone is None:
            g.current_timezone = get_timezone()





