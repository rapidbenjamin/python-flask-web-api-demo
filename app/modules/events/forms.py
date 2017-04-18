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

    price = DecimalField('price', default=0.0)

    user = QuerySelectField(query_factory=lambda: User.query.filter(User.is_active == True).all(), get_label="username", allow_blank=True)

    item = QuerySelectField(query_factory=lambda: Item.query.filter(Item.is_active == True).all(), get_label="slug", allow_blank=True)

    # start = DateField('start', format='%Y-%m-%d %H:%M:%S')
    start = DateField('start', format='%Y-%m-%d')

    # end = DateField('end', format='%Y-%m-%d %H:%M:%S')
    end = DateField('end', format='%Y-%m-%d')

    days = IntegerField('days', default=0)

    allday = BooleanField('allday', default=False)
    
    status = StringField('status', validators=[validators.Length(max=255, message='max 255 characters')])

    is_active = BooleanField('is_active', default=True)


