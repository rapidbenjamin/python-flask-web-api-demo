#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT LOCAL DEPENDENCIES  ------- your custom flask application 
from app import app


# ------- DEVELOPMENT CONFIG -------
if __name__ == '__main__':
    # app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(host='0.0.0.0', port=app.config['PORT'])



