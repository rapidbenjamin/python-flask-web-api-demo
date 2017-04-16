#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import datetime
from sqlalchemy import desc
from sqlalchemy import or_

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import db

import time
from app.helpers import *
from app.modules.localization.controllers import get_locale, get_timezone


# from app.modules.items.assetitem_model import AssetItem
# from app.modules.assets.models import Asset


class AssetItem(db.Model):
    __tablename__ = "assetitem"
    #__table_args__ = db.PrimaryKeyConstraint('asset_id', 'item_id')

    asset_id = db.Column(db.Integer,db.ForeignKey('Asset.id'), primary_key=True)
    item_id = db.Column(db.Integer,db.ForeignKey('Item.id'), primary_key=True)



    # bidirectional attribute/collection of "asset"/"assetitems" and "item"/"assetitems". Return object
    asset = db.relationship("Asset", back_populates = "assetitems")
    item = db.relationship("Item", back_populates ="assetitems")

    # so you can do :
    # assetitem1.append(Asset(assetname = 'test')))
    # or assetitem1.append(asset1)
    # or AssetItem(asset1, Item(title_en_US = 'test'), description_en_US="test")

    # Extra data
    description_en_US = db.Column(db.Text())
    description_fr_FR = db.Column(db.Text())


    updated_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()), onupdate=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))

    created_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    # updated_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()), onupdate=time.mktime(datetime.utcnow().timetuple())) 
    # created_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple())) 


    def __repr__(self):
        # return '<AssetItem: {}>'.format(self.id)
        return '<AssetItem %r - %r >' % (self.asset_id, self.item_id)





class Item(db.Model):
    __tablename__ = "Item"
    id = db.Column(db.Integer, primary_key=True)

    slug = db.Column(db.String(255), index=True, unique=True)

    title_en_US = db.Column(db.String(255),  index=True, unique=True)
    title_fr_FR = db.Column(db.String(255),  index=True, unique=True)

    description_en_US = db.Column(db.Text())
    description_fr_FR = db.Column(db.Text())

    # MANY-TO-MANY relationship with with EXTRA_DATA association and the Asset model
    # the cascade will delete orphaned assetitems
    assetitems = db.relationship('AssetItem', back_populates='item', lazy='dynamic', cascade="all, delete-orphan")
    # or Get all assets in view only mode 
    assets = db.relationship('Asset', secondary='assetitem', viewonly=True, back_populates='items', lazy='dynamic')
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
    WARNING : So don't use  directly asset.items.append(Item(title_en_US = 'test'))
                cause it's redundant, it will cause a duplicate INSERT on Association with 
                asset.assetitems.append(AssetItem(item=item1))
                add  viewonly=True on secondary relationship to stop edit, create or delete operations  here
    """

    # is_active usually returns True. 
    # This should return False only in cases where we have disabled item. 
    is_active = db.Column(db.Boolean, index=True, default=True)

    updated_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()), onupdate=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))

    created_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    # updated_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()), onupdate=time.mktime(datetime.utcnow().timetuple())) 
    # created_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple())) 


    def all_data(self, page, LISTINGS_PER_PAGE):
        return Item.query.order_by(desc(Item.created_at)).paginate(page, LISTINGS_PER_PAGE, False)

    def read_data(self, some_id):
        item = Item.query.filter(Item.id == some_id).first_or_404()
        return item


    def create_data(self, form):
        # dateTime conversion to timestamp
        timestamp_created_at = string_datetime_utc_to_string_timestamp_utc(form['created_at'])

        item = Item(
                                slug=form['slug'],

                                title_en_US=form['title_en_US'],
                                title_fr_FR=form['title_fr_FR'],

                                description_en_US=form['description_en_US'],
                                description_fr_FR=form['description_fr_FR'],

                                is_active = form['is_active'],
                                # convert string to integer format
                                created_at = int(timestamp_created_at)
                            )
        
        # MANY-TO-MANY Relationship
        for asset in form['assets']:
            assetitem = AssetItem(asset = asset, item = item)
            item.assetitems.append(assetitem)
        
        db.session.add(item)
        db.session.commit()

    def update_data(self, some_id, form ):
        item = Item.query.get_or_404(some_id)

        item.slug = form['slug']

        item.title_en_US = form['title_en_US']
        item.title_fr_FR = form['title_fr_FR']

        item.description_en_US = form['description_en_US']
        item.description_fr_FR = form['description_fr_FR']

        item.is_active = form['is_active']

        # dateTime conversion to timestamp
        timestamp_created_at = string_datetime_utc_to_string_timestamp_utc(form['created_at'])
        # convert string to integer format
        item.created_at = int(timestamp_created_at)

        # MANY-TO-MANY Relationship 
        item.assetitems = []
        for asset in form['assets']:
            assetitem = AssetItem(asset = asset, item = item)
            item.assetitems.append(assetitem)

        
        db.session.commit()

    def destroy_data(self, some_id ):
        item = Item.query.get_or_404(some_id)
        db.session.delete(item)
        db.session.commit()


    def __repr__(self):
        # return '<Item: {}>'.format(self.id)
        return '<Item %r>' % self.id


