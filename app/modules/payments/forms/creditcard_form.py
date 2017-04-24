#!/usr/bin/python
# -*- coding: utf-8 -*-

# import dependencies
from wtforms import Form, StringField, FileField, TextAreaField, validators, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField


from app.modules.users.models import User
from app.modules.orders.models import Order
from app.modules.payments.models.payment_model import Payment


class Form_Record_Add(Form):

    status = StringField('status', validators=[validators.Length(max=255, message='max 255 characters')])

    key_id = StringField('key_id', validators=[validators.Length(max=255, message='max 255 characters')])

    user = QuerySelectField(query_factory=lambda: User.query.filter(User.is_active == True).all(), get_label="username", allow_blank=True)

    type  = StringField('type', validators=[validators.Length(max=255, message='max 255 characters')])
    encrypted_number  = StringField('encrypted_number', validators=[validators.Length(max=255, message='max 255 characters')])
    expire_month  = StringField('expire_month', validators=[validators.Length(max=255, message='max 255 characters')])
    expire_year  = StringField('expire_year', validators=[validators.Length(max=255, message='max 255 characters')])
    first_name  = StringField('first_name', validators=[validators.Length(max=255, message='max 255 characters')])
    last_name  = StringField('last_name', validators=[validators.Length(max=255, message='max 255 characters')])

    params = TextAreaField('params', validators=[validators.Length(max=200, message='max 200 characters')])

    comments = TextAreaField('comments', validators=[validators.Length(max=200, message='max 200 characters')])


    is_active = BooleanField('is_active', default=True)
