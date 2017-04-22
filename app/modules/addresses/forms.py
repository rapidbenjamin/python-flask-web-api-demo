#!/usr/bin/python
# -*- coding: utf-8 -*-

# import dependencies
from wtforms import Form, StringField, TextAreaField, validators, BooleanField, DecimalField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

from app.modules.users.models import User
from app.modules.items.models import Item


# from app.modules.items.assetitem_model import AssetItem

class Form_Record_Add(Form):

    type = StringField('type', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])

    title_en_US = StringField('title_en_US', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])
    title_fr_FR = StringField('title_fr_FR', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])

    address_line1 = StringField('address_line1', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])
    address_line2 = StringField('address_line2', validators=[validators.Length(max=255, message='max 255 characters')])
    city = StringField('city', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])
    postal_code = StringField('postal_code', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])
    state_region = StringField('state_region', validators=[validators.Length(max=255, message='max 255 characters')])
    country = StringField('country', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])

    time_zone = StringField('time_zone', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])

    latitude = DecimalField('latitude', default=000.000000)
    longitude = DecimalField('longitude', default=000.000000)

    amount = DecimalField('amount', default=0.0)

    user = QuerySelectField(query_factory=lambda: User.query.filter(User.is_active == True).all(), get_label="username", allow_blank=True)
    
    item = QuerySelectField(query_factory=lambda: Item.query.filter(Item.is_active == True).all(), get_label="slug", allow_blank=True)


    # MANY-TO-MANY
    guests = QuerySelectMultipleField('Select Guests',
                             query_factory=lambda : User.query.filter(User.is_active == True).all(),
                             get_label=lambda u: u.username,
                             allow_blank=True)

    status = StringField('status', validators=[validators.Length(max=255, message='max 255 characters')])

    is_active = BooleanField('is_active', default=True)


