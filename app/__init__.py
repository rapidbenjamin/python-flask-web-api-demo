#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
from flask import Flask
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# ------- IMPORT LOCAL DEPENDENCIES ------- 
import os
from config import app_config


# ------- REGISTERS ------- 

# REGISTER ENVIRONMENT VARIABLES
# os.environ["FLASK_CONFIG"] = "development" or $ export FLASK_CONFIG=development
config_name = os.getenv('FLASK_CONFIG', 'default')

# REGISTER APPLICATION  
app = Flask(__name__, instance_relative_config=True)

# REGISTER CONFIGURATION TYPE    
app.config.from_object(app_config[config_name])
# REGISTER SENSITIVE CONFIG KEYS from the secret instance folder
app.config.from_pyfile(app_config[config_name].SECRET_CONFIG)


# REGISTER DATABASE
db = SQLAlchemy()
db.init_app(app)

# REGISTER LOGGING
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# REGISTER Migrate
migrate = Migrate(app, db)

# REGISTER LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"

# ------- IMPORT LOCAL DEPENDENCIES AFTER REGISTERING -------  
#To solve the problem from circular import, place the other imports which are dependent on 'db' and app below app== and db=SQLAlchemy(app).

# ------- LAST REGISTER MODULES WITH BLUEPRINTS -------  
from . import modules
from . import views
from modules.groups.models import Groups
from modules.users.models  import Users

# REGISTER BLUEPRINTS

from modules.home import home_page
app.register_blueprint(home_page, url_prefix='/home')

from modules.authentication import authentication_page
app.register_blueprint(authentication_page, url_prefix='/authentication')

from modules.admin import admin_page
app.register_blueprint(admin_page, url_prefix='/admin')

from modules.articles import articles_page
app.register_blueprint(articles_page, url_prefix='/articles')

from modules.groups import groups_page
app.register_blueprint(groups_page, url_prefix='/groups')

from modules.users import users_page
app.register_blueprint(users_page, url_prefix='/users')

from modules.contact import contact_page
app.register_blueprint(contact_page, url_prefix='/contact')



