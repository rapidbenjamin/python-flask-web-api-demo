#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
from flask import Blueprint
from flask.ext.babel import Babel

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app
from . import constants
from constants import *

# ADD CONSTANTS TO APP CONFIG
app.config['BABEL_DEFAULT_LOCALE'] = BABEL_DEFAULT_LOCALE
app.config['BABEL_DEFAULT_TIMEZONE'] = BABEL_DEFAULT_TIMEZONE
app.config['BABEL_TRANSLATION_DIRECTORIES'] = BABEL_TRANSLATION_DIRECTORIES
app.config['ALLOWED_LANGUAGES'] = ALLOWED_LANGUAGES


# REGISTER BABEL
babel = Babel(app)

# REGISTER MODULE
localization_service = Blueprint('localization_service', __name__, template_folder='templates', static_folder='static', static_url_path='/static')

# ------- IMPORT LOCAL DEPENDENCIES AFTER REGISTERING -------  
#To solve the problem from circular import, place the other imports which are dependent on 'babel' and app below app== and babel=Babel(app).

from . import controllers



