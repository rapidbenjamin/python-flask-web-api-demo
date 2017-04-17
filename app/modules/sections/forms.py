#!/usr/bin/python
# -*- coding: utf-8 -*-

# import dependencies
from wtforms import Form, StringField, TextAreaField, validators, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from app.modules.users.models import User
from app.modules.items.models import Item
from models import Section

# from app.modules.sections.usersection_model import UserSection

class Form_Record_Add(Form):

    slug = StringField('slug', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])


    parent = QuerySelectField(query_factory=lambda: Section.query.filter(Section.is_active == True).all(), get_label="slug", allow_blank=True)


    title_en_US = StringField('title_en_US', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])
    title_fr_FR = StringField('title_fr_FR', validators=[validators.DataRequired(),
                                             validators.Length(max=255, message='max 255 characters')])

    description_en_US = TextAreaField('description_en_US',
                                validators=[validators.Length(max=200, message='max 200 characters')])
    description_fr_FR = TextAreaField('description_fr_FR',
                                validators=[validators.Length(max=200, message='max 200 characters')])
    # MANY-TO-MANY
    users = QuerySelectMultipleField('Select Users',
                             query_factory=lambda : User.query.filter(User.is_active == True).all(),
                             get_label=lambda u: u.username,
                             allow_blank=True)

    items = QuerySelectMultipleField('Select Items',
                             query_factory=lambda : Item.query.filter(Item.is_active == True).all(),
                             get_label=lambda s: s.title_en_US,
                             allow_blank=True)

    is_active = BooleanField('is_active', default=True)

    # created_at = DateField('created_at', format='%Y-%m-%d %H:%M:%S')
    created_at = DateField('created_at', format='%Y-%m-%d')
