#!/usr/bin/python
# -*- coding: utf-8 -*-

# import dependencies
from wtforms import Form, StringField, TextAreaField, validators, BooleanField, DecimalField
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

from app.modules.sections.models import Section
from app.modules.assets.models import Asset
from app.modules.orders.models import Order
from app.modules.users.models import User

# from app.modules.items.assetitem_model import AssetItem

class Form_Record_Add(Form):

    slug = StringField('slug', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])

    price = DecimalField('price', default=0.0)

    title_en_US = StringField('title_en_US', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])
    title_fr_FR = StringField('title_fr_FR', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])

    description_en_US = TextAreaField('description_en_US',
                                validators=[validators.Length(max=200, message='max 200 characters')])
    description_fr_FR = TextAreaField('description_fr_FR',
                                validators=[validators.Length(max=200, message='max 200 characters')])

    user = QuerySelectField(query_factory=lambda: User.query.filter(User.is_active == True).all(), get_label="username", allow_blank=True)


    # MANY-TO-MANY
    sections = QuerySelectMultipleField('Select Sections',
                             query_factory=lambda : Section.query.filter(Section.is_active == True).all(),
                             get_label=lambda u: u.slug,
                             allow_blank=True)


    # MANY-TO-MANY
    assets = QuerySelectMultipleField('Select Assets',
                             query_factory=lambda : Asset.query.filter(Asset.is_active == True).all(),
                             get_label=lambda u: u.data_file_name,
                             allow_blank=True)

    # MANY-TO-MANY
    orders = QuerySelectMultipleField('Select Orders',
                             query_factory=lambda : Order.query.filter(Order.is_active == True).all(),
                             get_label=lambda u: u.id,
                             allow_blank=True)

    is_active = BooleanField('is_active', default=True)

    # created_at = DateField('created_at', format='%Y-%m-%d %H:%M:%S')
    created_at = DateField('created_at', format='%Y-%m-%d')
