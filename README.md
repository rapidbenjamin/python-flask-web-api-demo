Flask WEB API DEMO
========================


#### This is an advanced demo app forked from AndreiD/Flask-Easy-Template : https://github.com/AndreiD/Flask-Easy-Template

### Features:

- configuration files, environment variables and sensitive variables
- Utils for server production setups
- Latest bootstrap template, bootswatch, modernizer, jquery, moment.js, etc. served from content delivery networks.
- Module Sample home with Blueprint
- Module Sample articles/posts with Blueprints
- Module Sample users database with SQLALchemy and Pagination
- Module Sample groups 
- Module Sample contact form page with recaptcha and Email service by SendGrid
- SQLite or MySQL database option
- User Registry, Login, Logout,  & Forgot Password, etc.
- Flash messages notification
- Logger setting service
- Helpers (include decorators like SSL required, threaded function, random data generation sample)

#### Security :
You may have some sensitive variables that should not be publicly shared, such as passwords and secret keys. These can be put in an secrets/config.py file, which will not be pushed to version control.

#### How to use it:

- `git clone https://github.com/systemaker/flask-web-api-demo.git <project_name>` or download the zip
- `pip install -r requirements.txt` or `python -m pip install -r requirements-pip2.txt`
- `python run.py` -> http://server_ip:5000

#### Use it with configuration environment variable :
- `export FLASK_CONFIG=development` or in windows shell script `set FLASK_CONFIG=development`
- `export FLASK_APP=run.py` or in windows `set FLASK_APP=run.py`
- `flask run`

##### Things to do after:

- check the `config.py`
- in **run.py** edit the port of the app (Default: 5000)


- For templates edit `/app/templates/base.html`

    > <!DOCTYPE html>
    > {% set bootstrap_version = '3.3.4' %}
    > {% set jquery_version = '2.1.3' %}
    > {% set modernizer_version = '2.8.3' %}
    > {% set bootswatch_version = '3.3.2' %}
    > {% set bootswatch_theme = 'slate' %}

    In case you don't like the "slate" theme, you can chose a nice theme from http://bootswatch.com/ and just replace the theme name

- For DB migration use Flask-migrate
    type in console :
                    # create a migrations directory
                        - `export FLASK_CONFIG=development` or in windows shell script `set FLASK_CONFIG=development`
                        - `export FLASK_APP=run.py` or in windows `set FLASK_APP=run.py`
                        - `flask db init`
                    # create the first migration
                        - `flask db migrate`
                    # then apply the migration
                        - `flask db upgrade`

- To install a new package and save it on requirement file:
    `python -m pip install <new_package> && pip list > requirements.txt && pip list --format=freeze > requirements-pip2.txt`


- To remove all pyc files :
                         -  `find . -name \*.pyc -delete` or for windows users  `del /S *.pyc`


##### Extra configs for your server production environment : ./utils

- a supervisord.conf [supervisor is used to monitor the web application and restart it, also starts the app in case you restart your server]
- a simple nginx.conf
- after you go into production, uncomment the settings from run.py for the best performance

Your Feedback is appreciated :)

##### TROUBLESHOOTS FOR BEGINNERS :

    - READ FIRST : About Python 2 and 3 compatibility
    Some scripts and modules versions required here are written in python 2 and not ready yet for python 3 , 
    so it is recommended to download and install both interpreters python 2 and also python 3 (for windows users don't forget to add their folder paths also in your environment variables)
    Then when calling python scripts in version 2 or 3 anyway (example with the package manager script PIP), you can run default python command like :
        "python -m pip install ..." or "pip install ..."
    To call only python 3 scripts choose  this  instead :
        "py -m pip install ..." or "pip3 install ..."


    - Error parsing in requirements.txt ?
        Run instead this compatible formatted file :
            python -m pip install -r requirements-pip2.txt    
        or convert first your requirements.txt to a python 2 pip2 compatible format with this command :
            python -m pip list --format=freeze > requirements.txt


    - Error install on Proxytype : SyntaxError like Missing parentheses in call to 'print' ?
        the print function requires parentheses in Python 3 but not in Python 2 which means that the extension that you are trying to install is not yet compatible with python 3
        This is why it is recommended to install python 3 and python 2 by default.
        So run instead this compatible command for python 2 extensions (after installing python 2 if not got it yet) :
            python -m pip install -r requirements-pip2.txt
            or python -m pip install ...


    - Error install module Pycrypto : microsoft visual c++ compiler for python 2.7  is required ?
        download and install microsoft visual c++ compiler for python 2.7 here : https://www.microsoft.com/en-us/download/details.aspx?id=44266


    - Error Tornado module not found ? 
        it is a problem when installing modules like tornado in a multiple python interpreters environment 
        So run instead this common command python which precize by default  the python 2 version 
            python -m pip install -r requirements-pip2.txt
            or python -m pip install ...
            or python run.py
    
    - Error Install MySQL-python on Windows not working ?
        go over to oracle, and download the MySQL Connector C 6.0.2 and do the typical install.
        http://dev.mysql.com/downloads/connector/c/6.0.html#downloads


##### License: Apache 2.0

~~~~
Copyright 2017 Systemaker.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
~~~~
limitations under the License.
