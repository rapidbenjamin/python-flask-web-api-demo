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


class Groups(db.Model):
    __tablename__ = "Groups"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text())

    # one-to-many relationship with the User model
    users = db.relationship('Users', backref='group', lazy='dynamic')

    # is_active usually returns True. 
    # This should return False only in cases where we have disabled group. 
    is_active = db.Column(db.Boolean, index=True, default=True)

    updated_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()), onupdate=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))

    created_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    # updated_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()), onupdate=time.mktime(datetime.utcnow().timetuple())) 
    # created_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple())) 


    def all_data(self, page, LISTINGS_PER_PAGE):
        return Groups.query.order_by(desc(Groups.created_at)).paginate(page, LISTINGS_PER_PAGE, False)

    def read_data(self, some_id):
        group = Groups.query.filter(Groups.id == some_id).first_or_404()
        return group


    def create_data(self, form):
        # dateTime conversion to timestamp
        timestamp_created_at = string_datetime_utc_to_string_timestamp_utc(form['created_at'])

        new_record = Groups(
                                title=form['title'], 
                                description=form['description'],
                                is_active = form['is_active'],
                                # convert string to integer format
                                created_at = int(timestamp_created_at)
                            )
        db.session.add(new_record)
        db.session.commit()
    
    def update_data(self, some_id, form ):
        group = Groups.query.get_or_404(some_id)

        group.title = form['title']
        group.description = form['description']
        group.is_active = form['is_active']

        # dateTime conversion to timestamp
        timestamp_created_at = string_datetime_utc_to_string_timestamp_utc(form['created_at'])
        # convert string to integer format
        group.created_at = int(timestamp_created_at)


        db.session.commit()

    def delete_data(self, some_id ):
        group = Groups.query.get_or_404(some_id)
        db.session.delete(group)
        db.session.commit()


    def __repr__(self):
        # return '<Users: {}>'.format(self.id)
        return '<Groups %r>' % self.id
