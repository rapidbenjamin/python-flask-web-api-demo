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
from app.modules.localization.controllers import get_locale, get_timezone
# from app.modules.users.models import Users


class Sections(db.Model):
    __tablename__ = "Sections"
    id = db.Column(db.Integer, primary_key=True)

    slug = db.Column(db.String(255), index=True, unique=True)

    title_en_US = db.Column(db.String(255),  index=True, unique=True)
    title_fr_FR = db.Column(db.String(255),  index=True, unique=True)

    description_en_US = db.Column(db.Text(),  index=True)
    description_fr_FR = db.Column(db.Text(),  index=True)

    # one-to-many relationship with the User model
    users = db.relationship('Users', backref='section', lazy='dynamic')

    # is_active usually returns True. 
    # This should return False only in cases where we have disabled section. 
    is_active = db.Column(db.Boolean, index=True, default=True)

    updated_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()), onupdate=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))

    created_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    # updated_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()), onupdate=time.mktime(datetime.utcnow().timetuple())) 
    # created_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple())) 


    def all_data(self, page, LISTINGS_PER_PAGE):
        return Sections.query.order_by(desc(Sections.created_at)).paginate(page, LISTINGS_PER_PAGE, False)

    def read_data(self, some_id):
        section = Sections.query.filter(Sections.id == some_id).first_or_404()
        return section


    def create_data(self, form):
        # dateTime conversion to timestamp
        timestamp_created_at = string_datetime_utc_to_string_timestamp_utc(form['created_at'])

        new_record = Sections(
                                slug=form['slug'],

                                title_en_US=form['title_en_US'], 
                                title_fr_FR=form['title_fr_FR'], 

                                description_en_US=form['description_en_US'],
                                description_fr_FR=form['description_fr_FR'],

                                is_active = form['is_active'],
                                # convert string to integer format
                                created_at = int(timestamp_created_at)
                            )
        db.session.add(new_record)
        db.session.commit()
    
    def update_data(self, some_id, form ):
        section = Sections.query.get_or_404(some_id)

        section.slug = form['slug']

        section.title_en_US = form['title_en_US']
        section.title_fr_FR = form['title_fr_FR']

        section.description_en_US = form['description_en_US']
        section.description_fr_FR = form['description_fr_FR']

        section.is_active = form['is_active']

        # dateTime conversion to timestamp
        timestamp_created_at = string_datetime_utc_to_string_timestamp_utc(form['created_at'])
        # convert string to integer format
        section.created_at = int(timestamp_created_at)


        db.session.commit()

    def destroy_data(self, some_id ):
        section = Sections.query.get_or_404(some_id)
        db.session.delete(section)
        db.session.commit()


    def __repr__(self):
        # return '<Users: {}>'.format(self.id)
        return '<Sections %r>' % self.id
