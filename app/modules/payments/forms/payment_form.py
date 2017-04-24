#!/usr/bin/python
# -*- coding: utf-8 -*-

# import dependencies
from wtforms import Form, StringField, FileField, TextAreaField, validators, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField


from app.modules.users.models import User
from app.modules.orders.models import Order
from app.modules.payments.models.creditcard_model import Creditcard

class Form_Record_Add(Form):

    status = StringField('status', validators=[validators.Length(max=255, message='max 255 characters')])

    key_id = StringField('key_id', validators=[validators.Length(max=255, message='max 255 characters')])

    amount = DecimalField('amount', default=0.00)

    user = QuerySelectField(query_factory=lambda: User.query.filter(User.is_active == True).all(), get_label="username", allow_blank=True)

    order = QuerySelectField(query_factory=lambda: Order.query.filter(Order.is_active == True).all(), get_label="id", allow_blank=True)

    creditcard = QuerySelectField(query_factory=lambda: Creditcard.query.filter(Creditcard.is_active == True).all(), get_label="id", allow_blank=True)

    
    params = TextAreaField('params', validators=[validators.Length(max=200, message='max 200 characters')])

    comments = TextAreaField('comments', validators=[validators.Length(max=200, message='max 200 characters')])


    is_active = BooleanField('is_active', default=True)
