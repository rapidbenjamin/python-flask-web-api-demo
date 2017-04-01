#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app


# Localization I18N and l10n
BABEL_DEFAULT_LOCALE = "en_US"
BABEL_DEFAULT_TIMEZONE = "UTC"
# change path of messages.mo file
BABEL_TRANSLATION_DIRECTORIES = "app;static;localization"
ALLOWED_LANGUAGES = {
    'en_US': 'English',
    'fr_FR': 'French',
}





