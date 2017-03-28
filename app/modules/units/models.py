#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import datetime
from sqlalchemy import desc
from sqlalchemy import or_

# ------- IMPORT LOCAL DEPENDENCIES  -------
from ... import db

import time
from app.helpers import *
from app.localization import get_locale, get_timezone
# from app.modules.users.models import Users


class Units(db.Model):
    __tablename__ = "Units"
    id = db.Column(db.Integer, primary_key=True)
    title_en_US = db.Column(db.String(255), unique=True)
    description_en_US = db.Column(db.Text())

    title_fr_FR = db.Column(db.String(255), unique=True)
    description_fr_FR = db.Column(db.Text())

    # one-to-many relationship with the User model
    users = db.relationship('Users', backref='unit', lazy='dynamic')

    # is_active usually returns True. 
    # This should return False only in cases where we have disabled unit. 
    is_active = db.Column(db.Boolean, index=True, default=True)

    updated_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()), onupdate=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))

    created_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    # updated_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()), onupdate=time.mktime(datetime.utcnow().timetuple())) 
    # created_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple())) 


    def all_data(self, page, LISTINGS_PER_PAGE):
        return Units.query.order_by(desc(Units.created_at)).paginate(page, LISTINGS_PER_PAGE, False)

    def read_data(self, some_id):
        unit = Units.query.filter(Units.id == some_id).first_or_404()
        return unit


    def create_data(self, form):
        # dateTime conversion to timestamp
        timestamp_created_at = string_datetime_utc_to_string_timestamp_utc(form['created_at'])

        new_record = Units(
                                title_en_US=form['title_en_US'], 
                                description_en_US=form['description_en_US'],

                                title_fr_FR=form['title_fr_FR'], 
                                description_fr_FR=form['description_fr_FR'],

                                is_active = form['is_active'],
                                # convert string to integer format
                                created_at = int(timestamp_created_at)
                            )
        db.session.add(new_record)
        db.session.commit()
    
    def update_data(self, some_id, form ):
        unit = Units.query.get_or_404(some_id)

        unit.title_en_US = form['title_en_US']
        unit.description_en_US = form['description_en_US']

        unit.title_fr_FR = form['title_fr_FR']
        unit.description_fr_FR = form['description_fr_FR']

        unit.is_active = form['is_active']

        # dateTime conversion to timestamp
        timestamp_created_at = string_datetime_utc_to_string_timestamp_utc(form['created_at'])
        # convert string to integer format
        unit.created_at = int(timestamp_created_at)


        db.session.commit()

    def delete_data(self, some_id ):
        unit = Units.query.get_or_404(some_id)
        db.session.delete(unit)
        db.session.commit()


    def __repr__(self):
        # return '<Users: {}>'.format(self.id)
        return '<Units %r>' % self.id
