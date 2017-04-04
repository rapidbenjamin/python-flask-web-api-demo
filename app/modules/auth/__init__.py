#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
from flask import Blueprint
from flask_login import LoginManager

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app
from . import constants
from constants import *


# REGISTER LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)

# ADD CONSTANTS MESSAGE
login_manager.login_message = LOGIN_MESSAGE
login_manager.login_message_category = LOGIN_MESSAGE_CATEGORY
login_manager.login_controller = LOGIN_CONTROLLER

# REGISTER MODULE
auth_page = Blueprint('auth_page', __name__, template_folder='templates', static_folder='static', static_url_path='/static')

# ------- IMPORT LOCAL DEPENDENCIES AFTER REGISTERING -------  
#To solve the problem from circular import, place the other imports which are dependent on 'babel' and app below app== and babel=Babel(app).

from . import controllers, forms