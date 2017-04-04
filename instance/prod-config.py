#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import os
import binascii

# ------- IMPORT LOCAL DEPENDENCIES  -------

# absolute path for the parent directory of the directory your file is in
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

# a secret key should be as random as possible.
SECRET_KEY = 'p5Bv<6Zid2%$i01'
# TO GENERATE ONLY ONCE OTHERWISE YOU WILL GET MULTIPLE SESSIONS
    # SECRET_KEY = os.urandom(24).encode('hex')
    # SECRET_KEY = binascii.hexlify(os.urandom(24))

SQLALCHEMY_DATABASE_URI = 'mysql://systemaker:*systeMaker2017@localhost:3306/flask_web_api_db'

