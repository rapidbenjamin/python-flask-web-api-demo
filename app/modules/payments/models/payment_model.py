#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import datetime
import decimal
from sqlalchemy import desc
from sqlalchemy import or_
from flask import session
from flask_login import current_user

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import db

import time
from app.helpers import *
from app.modules.localization.controllers import get_locale, get_timezone

from app.modules.users.models import User
from app.modules.orders.models import Order



class Payment(db.Model):
    __tablename__ = "Payment"
    id = db.Column(db.Integer, primary_key=True)


    status = db.Column(db.String(30), index=True)

    # Credit card id key to get credit card credentials eventually available and stored in external remote api service
    key_id = db.Column(db.String(255), index=True)

    # MANY-TO-ONE relationship with the User model
    # the backref argument in the user field allows us to access payments from the User model
    # as simple as user.payments in our controllers.
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    # a bidirectional relationship in many-to-one. Return object
    user = db.relationship('User', back_populates='payments')

    # MANY-TO-ONE relationship with the Order model
    # the backref argument in the order field allows us to access payments from the Order model
    # as simple as order.payments in our controllers.
    order_id = db.Column(db.Integer, db.ForeignKey('Order.id'))
    # a bidirectional relationship in many-to-one. Return object
    order = db.relationship('Order', back_populates='payments')


    # MANY-TO-ONE relationship with the Creditcard model
    # the backref argument in the creditcard field allows us to access payments from the Creditcard model
    # as simple as creditcard.payments in our controllers.
    creditcard_id = db.Column(db.Integer, db.ForeignKey('Creditcard.id'))
    # a bidirectional relationship in many-to-one. Return object
    creditcard = db.relationship('Creditcard', back_populates='payments')

    ip_address =  db.Column(db.String(255))

    intent = db.Column(db.String(255))
    return_url = db.Column(db.String(255))
    cancel_url = db.Column(db.String(255))
    payment_method =  db.Column(db.String(255))
   


    # amount in decimal , precision=10, scale=2 .
    amount = db.Column(db.Numeric(10,2), nullable=False, default=0.0)
    currency = db.Column(db.String(255))




    params =  db.Column(db.Text())

    comments = db.Column(db.Text())

    # is_active usually returns True. 
    # This should return False only in cases where we have disabled payment. 
    is_active = db.Column(db.Boolean, index=True, default=True)

    updated_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()), onupdate=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))

    created_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    # updated_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()), onupdate=time.mktime(datetime.utcnow().timetuple())) 
    # created_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple())) 



    def all_data(self, page, LISTINGS_PER_PAGE):
        return Payment.query.order_by(desc(Payment.created_at)).paginate(page, LISTINGS_PER_PAGE, False)

    def read_data(self, some_id):
        payment = Payment.query.filter(Payment.id == some_id).first_or_404()
        return payment


    def create_data(self, form):

        payment = Payment(

                            status=form['status'],

                            key_id = form['key_id'],

                            amount = decimal.Decimal(form['amount']),

                            user = form['user'],

                            order = form['order'],

                            creditcard = form['creditcard'],

                            params  = form['params'],

                            comments = form['comments'],

                            is_active = form['is_active']

                        )

        if payment.order:
            payment.amount = payment.order.amount
        db.session.add(payment)
        db.session.commit()

    def update_data(self, some_id, form ):
        payment = Payment.query.get_or_404(some_id)

        payment.status =form['status']

        payment.key_id = form['key_id']

        payment.user = form['user']

        payment.order = form['order']

        payment.creditcard = form['creditcard']


        payment.params = form['params']

        payment.comments = form['comments']

        payment.is_active = form['is_active']


        if payment.order:
            payment.amount = payment.order.amount
        db.session.commit()

    def destroy_data(self, some_id ):
        payment = Payment.query.get_or_404(some_id)
        db.session.delete(payment)
        db.session.commit()


    def __repr__(self):
        # return '<User: {}>'.format(self.id)
        return '<Payment %r>' % self.id

