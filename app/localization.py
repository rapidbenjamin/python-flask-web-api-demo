#!/usr/bin/python
# -*- coding: utf-8 -*-


from flask import g, request
from dateutil import *
from dateutil import tz

# ------- IMPORT DEPENDENCIES -------

from . import app
from app import config_name, babel
from config import app_config


# @babel.localeselector
def get_locale():
    # the current user must be stored on the flask.g object.See example with flask-login : g.user = current_user
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale

    # otherwise you can get it by creating a global current language
    current_lang = getattr(g, 'current_lang', None)
    if current_lang is not None:
        return current_lang

    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support de/fr/en in this
    # example.  The best match wins.

    # return request.accept_languages.best_match(['de', 'fr', 'en'])
    return request.accept_languages.best_match(app_config[config_name].ALLOWED_LANGUAGES.keys())
    

# @babel.timezoneselector
def get_timezone():
    # the current user must be stored on the flask.g object.See example with flask-login : g.user = current_user
    # if a user is logged in, use the timezone from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone
     # otherwise you can get it by creating a global current language
    current_timezone = getattr(g, 'current_timezone', None)
    if current_timezone is not None:
        return current_timezone
    # otherwise auto detect timezone
    return  tz.tzlocal()

