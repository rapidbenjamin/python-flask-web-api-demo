#!/usr/bin/python
# -*- coding: utf-8 -*-

# import dependencies
from wtforms import Form, StringField, FileField, TextAreaField, validators, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField


from app.modules.users.models import User
from app.modules.items.models import Item
# from app.modules.items.assetitem_model import AssetItem

class Form_Record_Add(Form):

    status = StringField('status', validators=[validators.Length(max=255, message='max 255 characters')])

    user = QuerySelectField(query_factory=lambda: User.query.filter(User.is_active == True).all(), get_label="username", allow_blank=True)

    items = QuerySelectMultipleField('Select Items',
                             query_factory=lambda : Item.query.filter(Item.is_active == True).all(),
                             get_label=lambda s: s.title_en_US,
                             allow_blank=True)

    is_active = BooleanField('is_active', default=True)
