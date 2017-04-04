#!/usr/bin/python
# -*- coding: utf-8 -*-

# import dependencies
from wtforms import Form, StringField, FileField, TextAreaField, validators, BooleanField
from wtforms.fields.html5 import DateField


class Form_Record_Add(Form):

    assetable_id = StringField('assetable_id', validators=[validators.Length(max=255, message='max 255 characters')])
    assetable_type = StringField('assetable_type', validators=[validators.Length(max=255, message='max 255 characters')])

    data_file_name = FileField('data_file_name', validators=(validators.Optional(),))
    data_content_type = StringField('data_content_type', validators=[validators.Length(max=255, message='max 255 characters')])
    data_file_size = StringField('data_file_size', validators=[validators.Length(max=255, message='max 255 characters')])

    asset_type = StringField('asset_type', validators=[validators.Length(max=255, message='max 255 characters')])
    width = StringField('width', validators=[validators.Length(max=255, message='max 255 characters')])
    height = StringField('height', validators=[validators.Length(max=255, message='max 255 characters')])

    description_en_US = TextAreaField('description_en_US',
                                validators=[validators.Length(max=200, message='max 200 characters')])

    description_fr_FR = TextAreaField('description_fr_FR',
                                validators=[validators.Length(max=200, message='max 200 characters')])

    is_active = BooleanField('is_active')

    # created_at = DateField('created_at', format='%Y-%m-%d %H:%M:%S')
    created_at = DateField('created_at', format='%Y-%m-%d')
