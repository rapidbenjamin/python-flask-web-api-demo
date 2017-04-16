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
# from app.modules.users.models import User

# from app.modules.items.models import Item
# from app.modules.items.models import AssetItem



#######################
# WARNING FIXED ISSUE : AssetItem model registered at the end of this page to fixe issue  :  global name 'Asset' is not defined
#######################

class Asset(db.Model):
    __tablename__ = "Asset"
    id = db.Column(db.Integer, primary_key=True)

    data_file_name = db.Column(db.String(255))
    data_content_type = db.Column(db.String(255))
    data_file_size = db.Column(db.Integer)

    asset_type = db.Column(db.String(30), index=True)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)

    description_en_US = db.Column(db.Text())
    description_fr_FR = db.Column(db.Text())

    # one-to-many relationship with the User model
    users = db.relationship('User', back_populates='asset')


    # MANY-TO-MANY relationship with EXTRA_DATA columns association and the Item model
    # the cascade will delete orphaned assetitems
    assetitems = db.relationship('AssetItem', back_populates='asset', lazy='dynamic',  cascade="all, delete-orphan")
    # or  Get all items in view only mode
    items = db.relationship('Item', secondary='assetitem', viewonly=True, back_populates='assets', lazy='dynamic')

    """
    Return AssetItem objects collection
    and requires that child objects are associated with an association instance before being appended to the parent;
    similarly, access from parent to child goes through the association object:
    so to append items via association
        asset1.assetitems.append(AssetItem(item = Item(title_en_US = 'test')))

    or
        AssetItem(asset = asset1, Item(title_en_US = 'test'), extra_data="test")
    To iterate through items objects via association, including association attributes
        for assetitem in asset.assetitems:
            print(assetitem.extra_data)
            print(assetitem.item)
        or 
        for item in asset.items:
            print(item.title_en_US)
    WARNING : So don't use  directly asset.items.append(Item(title_en_US = 'test'))
                cause it's redundant, it will cause a duplicate INSERT on Association with 
                asset.assetitems.append(AssetItem(item=item1))
                add  viewonly=True on secondary relationship to stop edit, create or delete operations  here
    """


    # is_active usually returns True. 
    # This should return False only in cases where we have disabled asset. 
    is_active = db.Column(db.Boolean, index=True, default=True)

    updated_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()), onupdate=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))

    created_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    # updated_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()), onupdate=time.mktime(datetime.utcnow().timetuple())) 
    # created_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple())) 


    def all_data(self, page, LISTINGS_PER_PAGE):
        return Asset.query.order_by(desc(Asset.created_at)).paginate(page, LISTINGS_PER_PAGE, False)

    def read_data(self, some_id):
        asset = Asset.query.filter(Asset.id == some_id).first_or_404()
        return asset


    def create_data(self, form):
        # dateTime conversion to timestamp
        timestamp_created_at = string_datetime_utc_to_string_timestamp_utc(form['created_at'])

        new_record = Asset(    

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
        
        # MANY-TO-MANY Relationship 
        for item in form['items']:
            assetitem = AssetItem(asset = asset, item = item)
            asset.assetitems.append(assetitem)

        db.session.add(new_record)
        db.session.commit()
    
    def update_data(self, some_id, form ):
        asset = Asset.query.get_or_404(some_id)

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


        # MANY-TO-MANY Relationship
        asset.assetitems = []
        for item in form['items']:
            assetitem = AssetItem(item = item)
            asset.assetitems.append(assetitem)

        db.session.commit()

    def destroy_data(self, some_id ):
        asset = Asset.query.get_or_404(some_id)
        db.session.delete(asset)
        db.session.commit()


    def __repr__(self):
        # return '<User: {}>'.format(self.id)
        return '<Asset %r>' % self.id


#######################
# WARNING FIXED ISSUE : AssetItem model registered at the end of this page to fixe issue  :  global name 'Asset' is not defined
#######################

from app.modules.items.models import AssetItem