#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import os

# ------- IMPORT LOCAL DEPENDENCIES  -------


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """
    Common configurations
    Put any configurations here that are common across all environments
    """
    ADMIN_EMAIL = "your_email@gmail.com"

    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False

    SQLALCHEMY_DATABASE_URI = ''
    APP_NAME = 'Flask WEB API DEMO'
    SECRET_KEY = 'write-a-secret-string-here'
    LISTINGS_PER_PAGE = 5

    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = 'add_salt_123_hard_one'
    SECURITY_CONFIRMABLE = True


    # SendGrid example.
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'username'
    MAIL_PASSWORD = 'password'
    DEFAULT_MAIL_SENDER = 'notifications@your_website.com'
    SECURITY_EMAIL_SENDER = 'notifications@your_website.com'

    RECAPTCHA_SITE_KEY = "6Ldzx_Exxxxxxxxxxxxxxxxxxxxxxx"
    RECAPTCHA_SECRET = "6Ldzx_ESAAAxxxxxxxxxxxxxxxxxxxxxxxx"



class ProductionConfig(BaseConfig):
    """
    Production configurations
    """

    SECRET_CONFIG = 'prod-config.py'

    SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@server_ip:server_port/db_name'

    PORT = 5000
    DEBUG = False
    SQLALCHEMY_ECHO = False

class DevelopmentConfig(BaseConfig):
    """
    Development configurations
    """
    
    SECRET_CONFIG = 'dev-config.py'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data/db.sqlite')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

    PORT = 5000
    DEBUG = True

    # Allow SQLAlchemy to log errors
    SQLALCHEMY_ECHO = True 


class TestingConfig(BaseConfig):
    """
    Testing configurations
    """

    SECRET_CONFIG = 'test-config.py'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data/db.sqlite')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    TESTING = True


app_config = {  
    'default': DevelopmentConfig,  
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}