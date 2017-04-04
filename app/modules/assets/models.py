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


class Assets(db.Model):
    __tablename__ = "Assets"
    id = db.Column(db.Integer, primary_key=True)

    assetable_id = db.Column(db.Integer,  index=True)
    assetable_type = db.Column(db.String(30),  index=True)

    data_file_name = db.Column(db.String(255))
    data_content_type = db.Column(db.String(255))
    data_file_size = db.Column(db.Integer)

    asset_type = db.Column(db.String(30), index=True)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)

    description_en_US = db.Column(db.Text())
    description_fr_FR = db.Column(db.Text())

    # is_active usually returns True. 
    # This should return False only in cases where we have disabled asset. 
    is_active = db.Column(db.Boolean, index=True, default=True)

    updated_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()), onupdate=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))

    created_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    # updated_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()), onupdate=time.mktime(datetime.utcnow().timetuple())) 
    # created_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple())) 


    def all_data(self, page, LISTINGS_PER_PAGE):
        return Assets.query.order_by(desc(Assets.created_at)).paginate(page, LISTINGS_PER_PAGE, False)

    def read_data(self, some_id):
        asset = Assets.query.filter(Assets.id == some_id).first_or_404()
        return asset


    def create_data(self, form):
        # dateTime conversion to timestamp
        timestamp_created_at = string_datetime_utc_to_string_timestamp_utc(form['created_at'])

        new_record = Assets(    
                                assetable_id=form['assetable_id'], 
                                assetable_type=form['assetable_type'], 

                                data_file_name=form['data_file_name'], 
                                data_content_type=form['data_content_type'], 
                                data_file_size=form['data_file_size'], 

                                asset_type =form['asset_type'],
                                width=form['width'],
                                height=form['height'],

                                description_en_US=form['description_en_US'],
                                description_fr_FR=form['description_fr_FR'],

                                is_active = form['is_active'],
                                # convert string to integer format
                                created_at = int(timestamp_created_at)
                            )
        db.session.add(new_record)
        db.session.commit()
    
    def update_data(self, some_id, form ):
        asset = Assets.query.get_or_404(some_id)

        asset.assetable_id=form['assetable_id'] 
        asset.assetable_type=form['assetable_type'] 

        asset.data_file_name=form['data_file_name'] 
        asset.data_content_type=form['data_content_type'] 
        asset.data_file_size=form['data_file_size'] 

        asset.asset_type =form['asset_type']
        asset.width=form['width']
        asset.height=form['height']

        asset.description_en_US = form['description_en_US']
        asset.description_fr_FR = form['description_fr_FR']

        asset.is_active = form['is_active']

        # dateTime conversion to timestamp
        timestamp_created_at = string_datetime_utc_to_string_timestamp_utc(form['created_at'])
        # convert string to integer format
        asset.created_at = int(timestamp_created_at)


        db.session.commit()

    def destroy_data(self, some_id ):
        asset = Assets.query.get_or_404(some_id)
        db.session.delete(asset)
        db.session.commit()


    def __repr__(self):
        # return '<Users: {}>'.format(self.id)
        return '<Assets %r>' % self.id
