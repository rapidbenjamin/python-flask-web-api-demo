#!/usr/bin/python
# -*- coding: utf-8 -*-

# import dependencies
from wtforms import Form, StringField, TextAreaField, validators, BooleanField, DecimalField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

from app.modules.users.models import User
from app.modules.items.models import Item
from app.modules.addresses.models import Address


class Form_Record_Add(Form):

    type = StringField('type', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])

    title_en_US = StringField('title_en_US', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])
    title_fr_FR = StringField('title_fr_FR', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])

    description_en_US = TextAreaField('description_en_US',
                                validators=[validators.Length(max=200, message='max 200 characters')])
    description_fr_FR = TextAreaField('description_fr_FR',
                                validators=[validators.Length(max=200, message='max 200 characters')])

    amount = DecimalField('amount', default=0.0)

    user = QuerySelectField(query_factory=lambda: User.query.filter(User.is_active == True).all(), get_label="username", allow_blank=True)
    
    item = QuerySelectField(query_factory=lambda: Item.query.filter(Item.is_active == True).all(), get_label="item", allow_blank=True)

    address = QuerySelectField(query_factory=lambda: Address.query.filter(Address.is_active == True).all(), get_label="address", allow_blank=True)


     # MANY-TO-MANY
    guests = QuerySelectMultipleField('Select Guests',
                             query_factory=lambda : User.query.filter(User.is_active == True).all(),
                             get_label=lambda u: u.username,
                             allow_blank=True)

    # start = DateField('start', format='%Y-%m-%d %H:%M:%S')
    start = DateField('start', format='%Y-%m-%d')

    # end = DateField('end', format='%Y-%m-%d %H:%M:%S')
    end = DateField('end', format='%Y-%m-%d')


    allday = BooleanField('allday', default=False)
    
    status = StringField('status', validators=[validators.Length(max=255, message='max 255 characters')])

    is_active = BooleanField('is_active', default=True)


