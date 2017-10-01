#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import os
import redis
import binascii
from cryptography.fernet import Fernet

# ------- IMPORT LOCAL DEPENDENCIES  -------

# absolute path for the parent directory of the directory your file is in
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

# a secret key should be as random as possible.
SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# secret key used also for csrf_token
# TO GENERATE ONLY ONCE OTHERWISE YOU WILL GET MULTIPLE SESSIONS
    # SECRET_KEY = os.urandom(24).encode('hex')
    # SECRET_KEY = binascii.hexlify(os.urandom(24))

# Fernet key for encryption must be 32 url-safe base64-encoded bytes
# FERNET_SECRET_KEY = Fernet.generate_key()
FERNET_SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data/db.sqlite')
SQLALCHEMY_DATABASE_URI = 'mysql://user_name:password@localhost:3306/database_name'

# google map api key
GOOGLE_MAP_API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# SESSION REDIS    
SESSION_TYPE = 'redis'
# SESSION_TYPE = redis.Redis("redis")
SESSION_REDIS = redis.from_url('127.0.0.1:6379')


# Paypal config
PAYPAL_MODE = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # sandbox or live
PAYPAL_CLIENT_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
PAYPAL_CLIENT_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"