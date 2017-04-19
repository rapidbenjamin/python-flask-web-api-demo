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




class UserEvent(db.Model):
    __tablename__ = "userevent"
    #__table_args__ = db.PrimaryKeyConstraint('user_id', 'event_id')

    guest_id = db.Column(db.Integer,db.ForeignKey('User.id'), primary_key=True)
    in_event_id = db.Column(db.Integer,db.ForeignKey('Event.id'), primary_key=True)



    # bidirectional attribute/collection of "user"/"userevents" and "event"/"userevents". Return object
    guest = db.relationship("User", back_populates = "userevents")
    in_event = db.relationship("Event", back_populates ="userevents")

    # so you can do :
    # userevent1.append(User(username = 'test')))
    # or userevent1.append(user1)
    # or UserEvent(user1, Event(title_en_US = 'test'), options="test")

    # Extra data
    options = db.Column(db.Text())

    updated_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()), onupdate=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))

    created_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    # updated_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()), onupdate=time.mktime(datetime.utcnow().timetuple())) 
    # created_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple())) 


    def __repr__(self):
        # return '<UserEvent: {}>'.format(self.id)
        return '<UserEvent %r - %r >' % (self.guest_id, self.in_event_id)










class Event(db.Model):
    __tablename__ = "Event"
    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String(255), index=True)

    title_en_US = db.Column(db.String(255),  index=True, unique=True)
    title_fr_FR = db.Column(db.String(255),  index=True, unique=True)


    # amount in decimal , precision=10, scale=2 .
    amount = db.Column(db.Numeric(10,2), nullable=False, default=0.0)

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

    # MANY-TO-MANY relationship with with EXTRA_DATA association and the User model as Guest
    # the cascade will delete orphaned userevents
    userevents = db.relationship('UserEvent', back_populates='in_event', lazy='dynamic', cascade="all, delete-orphan")
    # or Get all users in view only mode 
    guests = db.relationship('User', secondary='userevent', viewonly=True, back_populates='in_events', lazy='dynamic')
    """
    Return UserEvent objects collection 
    and requires that child objects are associated with an association instance before being appended to the parent; 
    similarly, access from parent to child goes through the association object:
    so to append in_events via association
        guest1.guestdates.append(UserEvent(in_event = Event(title_en_US = 'test')))
        
    or 
        UserEvent(guest = guest1, Event(title_en_US = 'test'), extra_data="test")
    To iterate through in_events objects via association, including association attributes
        for guestdate in guest.guestdates:
            print(guestdate.extra_data)
            print(guestdate.in_event)
    WARNING : So don't use  directly guest.in_events.append(Event(title_en_US = 'test'))
                cause it's redundant, it will cause a duplicate INSERT on Association with 
                guest.guestdates.append(UserEvent(in_event=date1))
                add  viewonly=True on secondary relationship to stop edit, create or delete operations  here
    """

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

        calculate_days = (form['end'] - form['start']).days

        event = Event(
                                type = form['type'],

                                title_en_US=form['title_en_US'],
                                title_fr_FR=form['title_fr_FR'],

                                amount = decimal.Decimal(form['amount']),

                                user = form['user'],

                                item = form['item'],

                                # convert string to integer format
                                start = int(timestamp_start),

                                # convert string to integer format
                                end = int(timestamp_end),

                                # days = int(form['days']),
                                days = int(calculate_days),

                                allday = form['allday'],

                                status = form['status'],

                                is_active = form['is_active']

                            )

        # MANY-TO-MANY Relationship
        for guest in form['guests']:
            userevent = UserEvent(guest = guest, in_event = event)
            event.userevents.append(userevent)

        db.session.add(event)
        db.session.commit()

    def update_data(self, some_id, form ):
        event = Event.query.get_or_404(some_id)


        calculate_days = (form['end'] - form['start']).days

        event.type = form['type']

        event.title_en_US = form['title_en_US']
        event.title_fr_FR = form['title_fr_FR']

        event.amount = decimal.Decimal(form['amount'])

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

        # event.days = form['days']
        event.days = int(calculate_days)

        event.allday = form['allday']

        event.status = form['status']

        event.is_active = form['is_active']


        # MANY-TO-MANY Relationship 
        event.userevents = []
        for guest in form['guests']:
            userevent = UserEvent(guest = guest, in_event = event)
            event.userevents.append(userevent)


        db.session.commit()

    def destroy_data(self, some_id ):
        event = Event.query.get_or_404(some_id)
        db.session.delete(event)
        db.session.commit()


    def __repr__(self):
        # return '<Event: {}>'.format(self.id)
        return '<Event %r>' % self.id


