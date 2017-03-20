#!/usr/bin/python
# -*- coding: utf-8 -*-

# import dependencies
from wtforms import Form, StringField, TextAreaField, validators


class Form_Record_Add(Form):
    first_name = StringField('first_name', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])
    last_name = StringField('last_name',
                                validators=[validators.Length(max=255, message='max 255 characters')])
