#!/usr/bin/python
# -*- coding: utf-8 -*-

UPLOAD_FOLDER = '.app/static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# limit the maximum allowed payload to 16 megabytes. 
# If a larger file is transmitted, Flask will raise an RequestEntityTooLarge exception.
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

THUMBNAIL_SIZE = 128, 128
MAX_SIZE = 1600

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
# app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
# app.config['THUMBNAIL_SIZE'] = THUMBNAIL_SIZE
# app.config['MAX_SIZE'] = MAX_SIZE



# Localization I18N and l10n
BABEL_DEFAULT_LOCALE = "en_US"
BABEL_DEFAULT_TIMEZONE = "UTC"
# change path of messages.mo file
BABEL_TRANSLATION_DIRECTORIES = "app;static;localization"
ALLOWED_LANGUAGES = {
    'en_US': 'English',
    'fr_FR': 'French',
}