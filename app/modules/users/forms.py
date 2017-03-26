#!/usr/bin/python
# -*- coding: utf-8 -*-

# import dependencies
from wtforms import Form, StringField, TextAreaField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app.modules.groups.models import Groups

class Form_Record_Add(Form):
    email = StringField('email', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])
    username = StringField('username', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])
    group = QuerySelectField(query_factory=lambda: Groups.query.all(), get_label="title", allow_blank=True)
