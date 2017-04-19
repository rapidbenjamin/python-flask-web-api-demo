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


# ------- MANY-TO-MANY ASSOCIATION OBJECT : SECTION-ITEM  ------- 
class SectionItem(db.Model):
    __tablename__ = "sectionitem"
    #__table_args__ = db.PrimaryKeyConstraint('section_id', 'item_id')

    section_id = db.Column(db.Integer,db.ForeignKey('Section.id'), primary_key=True)
    item_id = db.Column(db.Integer,db.ForeignKey('Item.id'), primary_key=True)

    # bidirectional attribute/collection of "section"/"sectionitems" and "item"/"sectionitems". Return object
    section = db.relationship("Section", back_populates = "sectionitems")
    item = db.relationship("Item", back_populates ="sectionitems")

    # so you can do :
    # sectionitem1.append(Section(sectionname = 'test')))
    # or sectionitem1.append(section1)
    # or SectionItem(section1, Item(title_en_US = 'test'), description_en_US="test")

    # Extra data
    options = db.Column(db.Text())


    updated_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()), onupdate=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))

    created_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    # updated_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()), onupdate=time.mktime(datetime.utcnow().timetuple())) 
    # created_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple())) 


    def __repr__(self):
        # return '<SectionItem: {}>'.format(self.id)
        return '<SectionItem %r - %r >' % (self.section_id, self.item_id)



# ------- MANY-TO-MANY ASSOCIATION OBJECT : ASSET-ITEM  ------- 
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
    options = db.Column(db.Text())


    updated_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()), onupdate=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))

    created_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    # updated_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()), onupdate=time.mktime(datetime.utcnow().timetuple())) 
    # created_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple())) 


    def __repr__(self):
        # return '<AssetItem: {}>'.format(self.id)
        return '<AssetItem %r - %r >' % (self.asset_id, self.item_id)



# ------- MANY-TO-MANY ASSOCIATION OBJECT : ORDER-ITEM  ------- 
class OrderItem(db.Model):
    __tablename__ = "orderitem"
    #__table_args__ = db.PrimaryKeyConstraint('order_id', 'item_id')

    order_id = db.Column(db.Integer,db.ForeignKey('Order.id'), primary_key=True)
    item_id = db.Column(db.Integer,db.ForeignKey('Item.id'), primary_key=True)

    # bidirectional attribute/collection of "order"/"orderitems" and "item"/"orderitems". Return object
    order = db.relationship("Order", back_populates = "orderitems")
    item = db.relationship("Item", back_populates ="orderitems")

    # so you can do :
    # orderitem1.append(Order(ordername = 'test')))
    # or orderitem1.append(order1)
    # or OrderItem(order1, Item(title_en_US = 'test'), description_en_US="test")

    # EXTRA DATA
    options = db.Column(db.Text())

    # price in decimal , precision=10, scale=2
    unit_price = db.Column(db.Numeric(10,2), nullable=False)

    quantity = db.Column(db.Integer, nullable=False, default=1)

    # price in decimal , precision=10, scale=2 .
    total_price = db.Column(db.Numeric(10,2), nullable=False, default=0.0)


    updated_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()), onupdate=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))

    created_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    # updated_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()), onupdate=time.mktime(datetime.utcnow().timetuple())) 
    # created_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple())) 


    def __repr__(self):
        # return '<OrderItem: {}>'.format(self.id)
        return '<OrderItem %r - %r >' % (self.order_id, self.item_id)





class Item(db.Model):
    __tablename__ = "Item"
    id = db.Column(db.Integer, primary_key=True)

    slug = db.Column(db.String(255), index=True, unique=True)

    title_en_US = db.Column(db.String(255),  index=True, unique=True)
    title_fr_FR = db.Column(db.String(255),  index=True, unique=True)

    description_en_US = db.Column(db.Text())
    description_fr_FR = db.Column(db.Text())

    # price in decimal , precision=10, scale=2 .
    price = db.Column(db.Numeric(10,2), nullable=False, default=0.0)

    # one-to-many relationship with the Asset model
    events = db.relationship('Event', back_populates='item')

    # MANY-TO-ONE relationship with the User model
    # the backref argument in the user field allows us to access items from the User model
    # as simple as user.items in our controllers.
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    # a bidirectional relationship in many-to-one. Return object
    user = db.relationship('User', back_populates='items')

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

    # MANY-TO-MANY relationship with with EXTRA_DATA association and the Section model
    # the cascade will delete orphaned sectionitems
    sectionitems = db.relationship('SectionItem', back_populates='item', lazy='dynamic', cascade="all, delete-orphan")
    # or Get all sections in view only mode 
    sections = db.relationship('Section', secondary='sectionitem', viewonly=True, back_populates='items', lazy='dynamic')
    """
    Return SectionItem objects collection 
    and requires that child objects are associated with an association instance before being appended to the parent; 
    similarly, access from parent to child goes through the association object:
    so to append items via association
        section1.sectionitems.append(SectionItem(item = Item(title_en_US = 'test')))
        
    or 
        SectionItem(section = section1, Item(title_en_US = 'test'), extra_data="test")
    To iterate through items objects via association, including association attributes
        for sectionitem in section.sectionitems:
            print(sectionitem.extra_data)
            print(sectionitem.item)
    WARNING : So don't use  directly section.items.append(Item(title_en_US = 'test'))
                cause it's redundant, it will cause a duplicate INSERT on Association with 
                section.sectionitems.append(SectionItem(item=item1))
                add  viewonly=True on secondary relationship to stop edit, create or delete operations  here
    """

    # MANY-TO-MANY relationship with with EXTRA_DATA association and the Order model
    # the cascade will delete orphaned orderitems
    orderitems = db.relationship('OrderItem', back_populates='item', lazy='dynamic', cascade="all, delete-orphan")
    # or Get all orders in view only mode 
    orders = db.relationship('Order', secondary='orderitem', viewonly=True, back_populates='items', lazy='dynamic')
    """
    Return OrderItem objects collection 
    and requires that child objects are associated with an association instance before being appended to the parent; 
    similarly, access from parent to child goes through the association object:
    so to append items via association
        order1.orderitems.append(OrderItem(item = Item(title_en_US = 'test')))
        
    or 
        OrderItem(order = order1, Item(title_en_US = 'test'), extra_data="test")
    To iterate through items objects via association, including association attributes
        for orderitem in order.orderitems:
            print(orderitem.extra_data)
            print(orderitem.item)
    WARNING : So don't use  directly order.items.append(Item(title_en_US = 'test'))
                cause it's redundant, it will cause a duplicate INSERT on Association with 
                order.orderitems.append(OrderItem(item=item1))
                add  viewonly=True on secondary relationship to stop edit, create or delete operations  here
    """



    # is_active usually returns True. 
    # This should return False only in cases where we have disabled item. 
    is_active = db.Column(db.Boolean, index=True, nullable=False, default=1)

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

        item = Item(
                                slug=form['slug'],

                                title_en_US=form['title_en_US'],
                                title_fr_FR=form['title_fr_FR'],

                                description_en_US=form['description_en_US'],
                                description_fr_FR=form['description_fr_FR'],

                                price = decimal.Decimal(form['price']),

                                user = form['user'],

                                is_active = form['is_active'],

                            )
        
        # MANY-TO-MANY Relationship
        for section in form['sections']:
            sectionitem = SectionItem(section = section, item = item)
            item.sectionitems.append(sectionitem)
        
        # MANY-TO-MANY Relationship
        for asset in form['assets']:
            assetitem = AssetItem(asset = asset, item = item)
            item.assetitems.append(assetitem)
        
        # MANY-TO-MANY Relationship
        for order in form['orders']:
            # Do not calculate quantity and total price for order.amount when an item is just created
            orderitem = OrderItem(order = order, item = item)
            item.orderitems.append(orderitem)
        
        db.session.add(item)
        db.session.commit()

    def update_data(self, some_id, form ):
        item = Item.query.get_or_404(some_id)

        item.slug = form['slug']

        item.title_en_US = form['title_en_US']
        item.title_fr_FR = form['title_fr_FR']

        item.description_en_US = form['description_en_US']
        item.description_fr_FR = form['description_fr_FR']

        item.price = decimal.Decimal(form['price'])

        item.user = form['user']

        item.is_active = form['is_active']

        # MANY-TO-MANY Relationship 
        item.sectionitems = []
        for section in form['sections']:
            sectionitem = SectionItem(section = section, item = item)
            item.sectionitems.append(sectionitem)

        # MANY-TO-MANY Relationship 
        item.assetitems = []
        for asset in form['assets']:
            assetitem = AssetItem(asset = asset, item = item)
            item.assetitems.append(assetitem)

        # MANY-TO-MANY Relationship 
        item.orderitems = []
        for order in form['orders']:
            # DO not calculate again quantity and total price for order.amount, no updates when order already exist 
            orderitem = OrderItem(order = order, item = item)



            item.orderitems.append(orderitem)

        
        db.session.commit()

    def destroy_data(self, some_id ):
        item = Item.query.get_or_404(some_id)
        db.session.delete(item)
        db.session.commit()


    def __repr__(self):
        # return '<Item: {}>'.format(self.id)
        return '<Item %r>' % self.id


