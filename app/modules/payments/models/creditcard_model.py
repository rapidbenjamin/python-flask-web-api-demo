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
from app.modules.payments.models.payment_model import Payment


class Creditcard(db.Model):
    __tablename__ = "Creditcard"
    id = db.Column(db.Integer, primary_key=True)

    status = db.Column(db.String(30), index=True)

    # Credit card id key to get credit card credentials eventually available and stored in external remote api service
    key_id = db.Column(db.String(255), index=True)

    # MANY-TO-ONE relationship with the User model
    # the backref argument in the user field allows us to access payments from the User model
    # as simple as user.payments in our controllers.
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    # a bidirectional relationship in many-to-one. Return object
    user = db.relationship('User', back_populates='creditcards')


    # one-to-many relationship with the Payment model
    payments = db.relationship('Payment', back_populates='creditcard')


    type  = db.Column(db.String(255), index=True)
    # Always encrypt credit card number
    encrypted_number  = db.Column(db.Text())
    expire_month  = db.Column(db.Integer, index=True)
    expire_year  = db.Column(db.Integer, index=True)
    # Do not save cvv2 anywhere
    # cvv2  = ...
    first_name  = db.Column(db.String(255), index=True)
    last_name  = db.Column(db.String(255), index=True)


    params =  db.Column(db.Text())

    comments = db.Column(db.Text())

    # is_active usually returns True. 
    # This should return False only in cases where we have disabled creditcard.
    is_active = db.Column(db.Boolean, index=True, default=True)

    updated_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()), onupdate=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))

    created_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    # updated_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()), onupdate=time.mktime(datetime.utcnow().timetuple()))
    # created_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()))

    # Cryptography tool
    __encryptool = EncryptTool()

    def all_data(self, page, LISTINGS_PER_PAGE):
        return Creditcard.query.order_by(desc(Creditcard.created_at)).paginate(page, LISTINGS_PER_PAGE, False)

    def read_data(self, some_id):
        creditcard = Creditcard.query.filter(Creditcard.id == some_id).first_or_404()

        return creditcard


    def create_data(self, form):

        creditcard = Creditcard(

                            status=form['status'],

                            key_id = form['key_id'],

                            user = form['user'],

                            type  = form['type'],
                            encrypted_number  = form['encrypted_number'],
                            expire_month  = form['expire_month'],
                            expire_year  = form['expire_year'],
                            first_name  = form['first_name'],
                            last_name  = form['last_name'],

                            params  = form['params'],

                            comments = form['comments'],

                            is_active = form['is_active']

        )

        db.session.add(creditcard)
        db.session.commit()

    def update_data(self, some_id, form ):
        creditcard = Creditcard.query.get_or_404(some_id)

        creditcard.status =form['status']

        creditcard.key_id = form['key_id']

        creditcard.user = form['user']

        creditcard.type  = form['type']
        creditcard.encrypted_number  = form['encrypted_number']
        creditcard.expire_month  = form['expire_month']
        creditcard.expire_year  = form['expire_year']

        creditcard.first_name  = form['first_name']
        creditcard.last_name  = form['last_name']

        creditcard.params = form['params']
        creditcard.comments = form['comments']

        creditcard.is_active = form['is_active']

        db.session.commit()

    def destroy_data(self, some_id ):
        creditcard = Creditcard.query.get_or_404(some_id)
        db.session.delete(creditcard)
        db.session.commit()


    def __repr__(self):
        # return '<Creditcard: {}>'.format(self.id)
        return '<Creditcard %r>' % self.id


