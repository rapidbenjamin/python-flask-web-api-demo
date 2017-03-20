#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES -------
from threading import Thread
from functools import wraps
from flask import request, redirect, current_app

# ------- IMPORT LOCAL DEPENDENCIES ------- 
from modules.groups.models import Groups


# ------- DECORATORS -------
def threaded_async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def ssl_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if current_app.config.get("SSL"):
            if request.is_secure:
                return fn(*args, **kwargs)
            else:
                return redirect(request.url.replace("http://", "https://"))

        return fn(*args, **kwargs)

    return decorated_view



# ------- UTILS -------
def fill_db_with_random_data():
    # ---- example here with Groups model ----
    # ---- it might take some time ----

    from random import choice
    from string import printable
    import humanize
    import os
    start = time()
    lis = list(printable)
    for i in range(0, 50000):
        title = ''.join(choice(lis) for _ in xrange(5))
        description = ''.join(choice(lis) for _ in xrange(200))
        Groups().add_data(title, description)

    return "done in %.3f  | database size: %s" % (time() - start, humanize.naturalsize(os.path.getsize("data/db.sqlite")))

