#!/usr/bin/python
# -*- coding: utf-8 -*-

# import dependencies
from wtforms import Form, StringField, TextAreaField, BooleanField, validators
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app.modules.assets.models import Assets

class Form_Record_Add(Form):
    email = StringField('email', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])
    username = StringField('username', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])
    asset = QuerySelectField(query_factory=lambda: Assets.query.filter(Assets.is_active == True).all(), get_label="data_file_name", allow_blank=True)
    
    is_active = BooleanField('is_active')

    # created_at = DateField('created_at', format='%Y-%m-%d %H:%M:%S')
    created_at = DateField('created_at', format='%Y-%m-%d')