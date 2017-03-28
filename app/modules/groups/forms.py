#!/usr/bin/python
# -*- coding: utf-8 -*-

# import dependencies
from wtforms import Form, StringField, TextAreaField, validators, BooleanField
from wtforms.fields.html5 import DateField


class Form_Record_Add(Form):
    title = StringField('title', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])
    description = TextAreaField('description',
                                validators=[validators.Length(max=200, message='max 200 characters')])

    is_active = BooleanField('is_active')

    # created_at = DateField('created_at', format='%Y-%m-%d %H:%M:%S')
    created_at = DateField('created_at', format='%Y-%m-%d')
