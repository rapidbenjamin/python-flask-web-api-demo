#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import datetime
import decimal
import geocoder
from sqlalchemy import desc
from sqlalchemy import or_

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import db

import time
from app.helpers import *
from app.modules.localization.controllers import get_locale, get_timezone
from app.modules.users.models import User
from app.modules.items.models import Item




class UserAddress(db.Model):
    __tablename__ = "useraddress"
    #__table_args__ = db.PrimaryKeyConstraint('user_id', 'address_id')

    guest_id = db.Column(db.Integer,db.ForeignKey('User.id'), primary_key=True)
    in_address_id = db.Column(db.Integer,db.ForeignKey('Address.id'), primary_key=True)



    # bidirectional attribute/collection of "user"/"useraddresses" and "address"/"useraddresses". Return object
    guest = db.relationship("User", back_populates = "useraddresses")
    in_address = db.relationship("Address", back_populates ="useraddresses")

    # so you can do :
    # useraddress1.append(User(username = 'test')))
    # or useraddress1.append(user1)
    # or UserAddress(user1, Address(title_en_US = 'test'), options="test")

    # Extra data
    options = db.Column(db.Text())

    updated_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()), onupdate=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))

    created_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    # updated_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()), onupdate=time.mktime(datetime.utcnow().timetuple())) 
    # created_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple())) 


    def __repr__(self):
        # return '<UserAddress: {}>'.format(self.id)
        return '<UserAddress %r - %r >' % (self.guest_id, self.in_address_id)










class Address(db.Model):
    __tablename__ = "Address"
    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String(255), index=True)

    title_en_US = db.Column(db.String(255),  index=True, unique=True)
    title_fr_FR = db.Column(db.String(255),  index=True, unique=True)

    address_line1 = db.Column(db.String(255),  index=True)
    address_line2 = db.Column(db.String(255),  index=True)
    city = db.Column(db.String(255),  index=True)
    postal_code = db.Column(db.String(255),  index=True)
    state_region = db.Column(db.String(255),  index=True)
    country = db.Column(db.String(255),  index=True)
    country_code = db.Column(db.String(255),  index=True)
    full = db.Column(db.String(255),  index=True)
    time_zone = db.Column(db.String(255),  index=True)


    latitude = db.Column(db.Numeric(9,6), index=True, nullable=False, default=000.000000)
    longitude = db.Column(db.Numeric(9,6), index=True, nullable=False, default=000.000000)

    # amount in decimal , precision=10, scale=2 .
    amount = db.Column(db.Numeric(10,2), nullable=False, default=0.0)

    # MANY-TO-ONE relationship with the User model
    # the backref argument in the user field allows us to access addresses from the User model
    # as simple as user.addresses in our controllers.
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    # a bidirectional relationship in many-to-one. Return object
    user = db.relationship('User', back_populates='addresses')

    # MANY-TO-ONE relationship with the Item model
    # the backref argument in the item field allows us to access addresses from the Item model
    # as simple as item.addresses in our controllers.
    item_id = db.Column(db.Integer, db.ForeignKey('Item.id'))
    # a bidirectional relationship in many-to-one. Return object
    item = db.relationship('Item', back_populates='addresses')

    # one-to-many relationship with the Event model
    events = db.relationship('Event', back_populates='address')

    # MANY-TO-MANY relationship with with EXTRA_DATA association and the User model as Guest
    # the cascade will delete orphaned useraddresses
    useraddresses = db.relationship('UserAddress', back_populates='in_address', lazy='dynamic', cascade="all, delete-orphan")
    # or Get all users in view only mode 
    guests = db.relationship('User', secondary='useraddress', viewonly=True, back_populates='in_addresses', lazy='dynamic')
    """
    Return UserAddress objects collection 
    and requires that child objects are associated with an association instance before being appended to the parent; 
    similarly, access from parent to child goes through the association object:
    so to append in_addresses via association
        guest1.guestdates.append(UserAddress(in_address = Address(title_en_US = 'test')))
        
    or 
        UserAddress(guest = guest1, Address(title_en_US = 'test'), extra_data="test")
    To iterate through in_addresses objects via association, including association attributes
        for guestdate in guest.guestdates:
            print(guestdate.extra_data)
            print(guestdate.in_address)
    WARNING : So don't use  directly guest.in_addresses.append(Address(title_en_US = 'test'))
                cause it's redundant, it will cause a duplicate INSERT on Association with 
                guest.guestdates.append(UserAddress(in_address=date1))
                add  viewonly=True on secondary relationship to stop edit, create or delete operations  here
    """


    status = db.Column(db.String(255), index=True)

    # is_active usually returns True. 
    # This should return False only in cases where we have disabled address. 
    is_active = db.Column(db.Boolean, index=True, nullable=False, default=1)

    updated_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()), onupdate=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))

    created_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    # updated_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()), onupdate=time.mktime(datetime.utcnow().timetuple())) 
    # created_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple())) 


    def all_data(self, page, LISTINGS_PER_PAGE):
        return Address.query.order_by(desc(Address.created_at)).paginate(page, LISTINGS_PER_PAGE, False)

    def read_data(self, some_id):
        address = Address.query.filter(Address.id == some_id).first_or_404()
        return address


    def create_data(self, form):

        full = ""
        if form['address_line1']:
            full += form['address_line1'] + ', '
        if form['address_line2']:
            full += form['address_line2']  + ', '
        if form['city']:
            full += form['city']  + ', '
        if form['postal_code']:
            full += form['postal_code']  + ', '
        if form['state_region']:
            full += form['state_region']  + ', '
        if form['country']:
            full += form['country']

        geoc = geocoder.google(full)

        # If request denied : Missing api key google map
        if geoc.latlng:
            latitude, longitude = geoc.latlng
        else:
            latitude = decimal.Decimal(form['latitude'])
            longitude = decimal.Decimal(form['longitude'])

        address = Address(
                                type = form['type'],

                                title_en_US = form['title_en_US'],
                                title_fr_FR = form['title_fr_FR'],

                                address_line1 = form['address_line1'],
                                address_line2 = form['address_line2'],
                                city = form['city'],
                                postal_code = form['postal_code'],
                                state_region = form['state_region'],
                                country = form['country'],
                                country_code = form['country_code'],
                                # full = form['full'],
                                full = full,
                                time_zone = form['time_zone'],

                                # latitude = decimal.Decimal(form['latitude']),
                                # longitude = decimal.Decimal(form['longitude']),

                                latitude = latitude,
                                longitude = longitude,

                                amount = decimal.Decimal(form['amount']),

                                user = form['user'],

                                item = form['item'],

                                status = form['status'],

                                is_active = form['is_active']

                            )

        # MANY-TO-MANY Relationship
        for guest in form['guests']:
            useraddress = UserAddress(guest = guest, in_address = address)
            address.useraddresses.append(useraddress)

        db.session.add(address)
        db.session.commit()

    def update_data(self, some_id, form ):

        full = ""
        if form['address_line1']:
            full += form['address_line1'] + ', '
        if form['address_line2']:
            full += form['address_line2']  + ', '
        if form['city']:
            full += form['city']  + ', '
        if form['postal_code']:
            full += form['postal_code']  + ', '
        if form['state_region']:
            full += form['state_region']  + ', '
        if form['country']:
            full += form['country']

        geoc = geocoder.google(full)


        # If request denied : Missing api key google map
        if geoc.latlng:
            latitude, longitude = geoc.latlng
        else:
            latitude = decimal.Decimal(form['latitude'])
            longitude = decimal.Decimal(form['longitude'])
        
        


        address = Address.query.get_or_404(some_id)


        address.type = form['type']

        address.title_en_US = form['title_en_US']
        address.title_fr_FR = form['title_fr_FR']

        address.address_line1 = form['address_line1']
        address.address_line2 = form['address_line2']
        address.city = form['city']
        address.postal_code = form['postal_code']
        address.state_region = form['state_region']
        address.country = form['country']
        address.country_code = form['country_code']
        address.full = full
        address.time_zone = form['time_zone']

        #address.latitude = decimal.Decimal(form['latitude'])
        #address.longitude = decimal.Decimal(form['longitude'])

        address.latitude = latitude
        address.longitude = longitude

        address.amount = decimal.Decimal(form['amount'])

        address.user = form['user']

        address.item = form['item']

        address.status = form['status']

        address.is_active = form['is_active']


        # MANY-TO-MANY Relationship 
        address.useraddresses = []
        for guest in form['guests']:
            useraddress = UserAddress(guest = guest, in_address = address)
            address.useraddresses.append(useraddress)


        db.session.commit()

    def destroy_data(self, some_id ):
        address = Address.query.get_or_404(some_id)
        db.session.delete(address)
        db.session.commit()


    def __repr__(self):
        # return '<Address: {}>'.format(self.id)
        return '<Address %r>' % self.id


