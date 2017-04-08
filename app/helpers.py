#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES -------
from datetime import *
from dateutil import *
from dateutil import tz
import time
from jinja2 import Environment
import os
import binascii

# ------- IMPORT LOCAL DEPENDENCIES -------
from threading import Thread
from functools import wraps
from flask import request, redirect, current_app
from . import app






# ------- DECORATORS -------
def threaded_async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def ssl_required(fn):
    @wraps(fn)
    def decorated_controller(*args, **kwargs):
        if current_app.config.get("SSL"):
            if request.is_secure:
                return fn(*args, **kwargs)
            else:
                return redirect(request.url.replace("http://", "https://"))

        return fn(*args, **kwargs)

    return decorated_controller


# ------- RANDOM TOKEN GENERATOR -------
def generate_token():
    # a secret key should be as random as possible.
    token = binascii.hexlify(os.urandom(24))
    return token

# ------- RANDOM POPULATE DATABASE -------
def populate_db_with_random_data(db_model):
    # ---- example here with a db model ----
    # ---- it might take some time ----

    from random import choice
    from string import printable
    import humanize
    import os
    start = time()
    lis = list(printable)
    for i in range(0, 50000):
        for k,v in db_model():
            short_value_list = ['title', 'name', 'password']
            long_value_list = ['description']
            if short_value_list in k :
                k = ''.join(choice(lis) for _ in xrange(5))
            if long_value_list in k :
                k = ''.join(choice(lis) for _ in xrange(200))
            db_model().add_data(k)

    return "done in %.3f  | database size: %s" % (time() - start, humanize.naturalsize(os.path.getsize("data/db.sqlite")))


# ------- DATETIME UTILS -------

def datetime_string_to_datetime_obj(datetime_string, strftime):
	# Convert datetime string to datetime obj with his format described in strftime argument function
	datetime_obj = datetime.strptime(datetime_string, strftime )
    # print type(datetime_obj)
	return datetime_obj

def datetime_obj_to_datetime_string(datetime_obj, strftime = '%Y-%m-%d %H:%M:%S %H:%M:%S'):
	# Generate UTC datetime string
	datetime_string = datetime_obj.strftime(strftime)
    # print type(datetime_string)
	return datetime_string

def datetime_local_to_datetime_utc(datetime_local):
	# Hardcode utc zone 
	utc_zone = tz.gettz('UTC') 
	# or Auto-detect utc zone
	# utc_zone = tz.tzutc()
	
    # Convert local time to UTC
	datetime_utc = datetime_local.astimezone(utc_zone)
    # print type(datetime_utc)
	return datetime_utc

def datetime_utc_to_datetime_local(datetime_utc, local_zone = None):
	
	if local_zone is None : 
		# Hardcode local zone 
		# local_zone = tz.gettz('America/Chicago')
		# or Auto-detect local zone
		local_zone = tz.tzlocal()
	
    # Tell the datetime object that it's in local time zone since 
	# datetime objects are 'naive' by default
	datetime_local = datetime_utc.replace(tzinfo=local_zone)
    # print type(datetime_local)
	return datetime_local
	
def string_timestamp_utc_to_string_datetime_utc(timestamp_utc, strftime = '%Y-%m-%d %H:%M:%S'):
	datetime_utc = datetime.fromtimestamp(timestamp_utc).strftime(strftime)
    # print type(datetime_utc)
	return datetime_utc

def string_datetime_utc_to_string_timestamp_utc(datetime_utc):
    # timetuple() convert datetime obj to timestamp obj
    # time.mktime convert timestamp obj to timestamp string
	timestamp_utc = time.mktime(datetime_utc.timetuple())
    # print type(timestamp_utc)
	return timestamp_utc

# Create Jinja new filter
def datetimeformat(date, format='%Y-%m-%d %H:%M:%S'):
    return string_timestamp_utc_to_string_datetime_utc(date, format)

app.jinja_env.filters['datetimeformat'] = datetimeformat