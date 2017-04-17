#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import tornado
from tornado import autoreload
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging


# ------- IMPORT LOCAL DEPENDENCIES  ------- your custom flask application 
from app import app





# INITIALIZE
enable_pretty_logging()


# ------- PRODUCTION CONFIG -------
# http_server = HTTPServer(WSGIContainer(app))
# http_server.bind(app.config['PORT'])
# http_server.start(0)
# ioloop = tornado.ioloop.IOLoop().instance()
# autoreload.start(ioloop)
# ioloop.start()


# ------- DEVELOPMENT CONFIG -------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['PORT'])



