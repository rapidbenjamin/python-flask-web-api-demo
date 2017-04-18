#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import datetime
import decimal
from sqlalchemy import desc
from sqlalchemy import or_

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import db

import time
from app.helpers import *
from app.modules.localization.controllers import get_locale, get_timezone
from app.modules.users.models import User
from app.modules.items.models import Item

class Event(db.Model):
    __tablename__ = "Event"
    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String(255), index=True)

    # price in decimal , precision=10, scale=2 .
    price = db.Column(db.Numeric(10,2), nullable=False, default=0.0)

    # MANY-TO-ONE relationship with the User model
    # the backref argument in the user field allows us to access events from the User model
    # as simple as user.events in our controllers.
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    # a bidirectional relationship in many-to-one. Return object
    user = db.relationship('User', back_populates='events')

    # MANY-TO-ONE relationship with the Item model
    # the backref argument in the item field allows us to access events from the Item model
    # as simple as item.events in our controllers.
    item_id = db.Column(db.Integer, db.ForeignKey('Item.id'))
    # a bidirectional relationship in many-to-one. Return object
    item = db.relationship('Item', back_populates='events')


    start = db.Column(db.Integer, index=True)

    end = db.Column(db.Integer, index=True)

    days = db.Column(db.Integer, index=True)

    allday = db.Column(db.Boolean, index=True)

    status = db.Column(db.String(255), index=True)

    # is_active usually returns True. 
    # This should return False only in cases where we have disabled event. 
    is_active = db.Column(db.Boolean, index=True, nullable=False, default=1)

    updated_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()), onupdate=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))

    created_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    # updated_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()), onupdate=time.mktime(datetime.utcnow().timetuple())) 
    # created_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple())) 


    def all_data(self, page, LISTINGS_PER_PAGE):
        return Event.query.order_by(desc(Event.created_at)).paginate(page, LISTINGS_PER_PAGE, False)

    def read_data(self, some_id):
        event = Event.query.filter(Event.id == some_id).first_or_404()
        return event


    def create_data(self, form):
        # dateTime conversion to timestamp
        timestamp_start = string_datetime_utc_to_string_timestamp_utc(form['start'])
        timestamp_end = string_datetime_utc_to_string_timestamp_utc(form['end'])

        event = Event(
                                type = form['type'],

                                price = decimal.Decimal(form['price']),

                                user = form['user'],

                                item = form['item'],

                                # convert string to integer format
                                start = int(timestamp_start),

                                # convert string to integer format
                                end = int(timestamp_end),

                                days = int(form['days']),

                                allday = form['allday'],

                                status = form['status'],

                                is_active = form['is_active'],

                            )

        db.session.add(event)
        db.session.commit()

    def update_data(self, some_id, form ):
        event = Event.query.get_or_404(some_id)

        event.type = form['type']

        event.price = decimal.Decimal(form['price'])

        event.user = form['user']

        event.item = form['item']

        # dateTime conversion to timestamp
        timestamp_start = string_datetime_utc_to_string_timestamp_utc(form['start'])
        # convert string to integer format
        event.start = int(timestamp_start)

        # dateTime conversion to timestamp
        timestamp_end = string_datetime_utc_to_string_timestamp_utc(form['end'])
        # convert string to integer format
        event.end = int(timestamp_end)

        event.days = form['days']

        event.allday = form['allday']

        event.status = form['status']

        event.is_active = form['is_active']

        db.session.commit()

    def destroy_data(self, some_id ):
        event = Event.query.get_or_404(some_id)
        db.session.delete(event)
        db.session.commit()


    def __repr__(self):
        # return '<Event: {}>'.format(self.id)
        return '<Event %r>' % self.id


