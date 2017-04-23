#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import datetime
import decimal
from sqlalchemy import desc
from sqlalchemy import or_
from flask import session
from flask_login import current_user

# ------- IMPORT LOCAL DEPENDENCIES  -------
from ... import db

import time
from app.helpers import *
from app.modules.localization.controllers import get_locale, get_timezone
from app.modules.users.models import User

from app.modules.items.models import Item
# from app.modules.items.models import OrderItem



#######################
# WARNING FIXED ISSUE : OrderItem model registered at the end of this page to fixe issue  :  global name 'Order' is not defined
#######################

class Order(db.Model):
    __tablename__ = "Order"
    id = db.Column(db.Integer, primary_key=True)


    status = db.Column(db.String(30), index=True)

    # MANY-TO-ONE relationship with the User model
    # the backref argument in the user field allows us to access orders from the User model
    # as simple as user.orders in our controllers.
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    # a bidirectional relationship in many-to-one. Return object
    user = db.relationship('User', back_populates='orders')


    # MANY-TO-MANY relationship with EXTRA_DATA columns association and the Item model
    # the cascade will delete orphaned orderitems
    orderitems = db.relationship('OrderItem', back_populates='order', lazy='dynamic',  cascade="all, delete-orphan")
    # or  Get all items in view only mode
    items = db.relationship('Item', secondary='orderitem', viewonly=True, back_populates='orders', lazy='dynamic')

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
        or 
        for item in order.items:
            print(item.title_en_US)
    WARNING : So don't use  directly order.items.append(Item(title_en_US = 'test'))
                cause it's redundant, it will cause a duplicate INSERT on Association with 
                order.orderitems.append(OrderItem(item=item1))
                add  viewonly=True on secondary relationship to stop edit, create or delete operations  here
    """

    # amount in decimal , precision=10, scale=2 .
    amount = db.Column(db.Numeric(10,2), nullable=False, default=0.0)

    params =  db.Column(db.Text())

    comments = db.Column(db.Text())

    # is_active usually returns True. 
    # This should return False only in cases where we have disabled order. 
    is_active = db.Column(db.Boolean, index=True, default=True)

    updated_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()), onupdate=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))

    created_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    # updated_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()), onupdate=time.mktime(datetime.utcnow().timetuple())) 
    # created_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple())) 


    def current_order(self):
        if session.get('order_id') :
            this_order = Order.query.filter(Order.id == int(session.get('order_id'))).first()
            return this_order
        else:
            new_order = Order()
            new_order.status = 'cart'
            new_order.is_active = True
            db.session.add(new_order)
            db.session.commit()
            session['order_id'] = new_order.id
            return new_order


    def add_cart(self, item_id, request_args):
        # MANY-TO-MANY Relationship

        order =  self.current_order()

        amount = decimal.Decimal(order.amount)
        item = Item.query.filter(Item.id == item_id).first_or_404()
        
        # if item already exist
        if order.orderitems:
            for orderitem in order.orderitems :
                if orderitem.item_id == item.id:
                    # Update amount
                    if request_args and 'quantity' in request_args:                    
                        orderitem.quantity = orderitem.quantity + int(request_args['quantity'])
                        if orderitem.quantity <= 0:
                            orderitem.quantity = 1
                        order.amount = order.amount - orderitem.total_amount
                        orderitem.total_amount = orderitem.unit_amount * orderitem.quantity
                        order.amount = order.amount + orderitem.total_amount
                    
                    db.session.add(order)
                    db.session.commit()
                    return order


        # if new item
        orderitem = OrderItem(order = order, item = item)
        
        # Caculate amount
        orderitem.unit_amount = item.amount
        if request_args and 'quantity' in request_args:
            orderitem.quantity = int(request_args['quantity'])
        else:
            orderitem.quantity = 1
        orderitem.total_amount = orderitem.unit_amount * orderitem.quantity
        amount = amount +  orderitem.total_amount
        order.orderitems.append(orderitem)
        order.amount = amount
        if current_user and not order.user :
            order.user = current_user
        db.session.add(order)
        db.session.commit()
        return order



    def update_cart(self, item_id, request_args):

        # MANY-TO-MANY Relationship
        order =  self.current_order()

        amount = decimal.Decimal(order.amount)

        item = Item.query.filter(Item.id == item_id).first_or_404()

        # order.items.remove(item)

        for orderitem in order.orderitems :
            if orderitem.item.id == item.id:
                # Update amount with request.args variables like quantity, options, unit_amount
                if request_args and 'quantity' in request_args:                    
                    orderitem.quantity = orderitem.quantity + int(request_args['quantity'])
                    if orderitem.quantity <= 0:
                        orderitem.quantity = 1
                    order.amount = order.amount - orderitem.total_amount
                    orderitem.total_amount = orderitem.unit_amount * orderitem.quantity
                    order.amount = order.amount + orderitem.total_amount

        db.session.add(order)
        db.session.commit()
        return order
        

    def remove_cart(self, item_id):
        # MANY-TO-MANY Relationship
        
        order =  self.current_order()

        amount = decimal.Decimal(order.amount)

        item = Item.query.filter(Item.id == item_id).first_or_404()

        # order.items.remove(item)

        for orderitem in order.orderitems :
            if orderitem.item.id == item.id:
                order.amount = order.amount - orderitem.total_amount
                order.orderitems.remove(orderitem)
        db.session.commit()
        return order






    def all_data(self, page, LISTINGS_PER_PAGE):
        return Order.query.order_by(desc(Order.created_at)).paginate(page, LISTINGS_PER_PAGE, False)

    def read_data(self, some_id):
        order = Order.query.filter(Order.id == some_id).first_or_404()
        return order


    def create_data(self, form):

        order = Order(

                            status=form['status'],

                            user = form['user'],

                            is_active = form['is_active']

                        )

        # MANY-TO-MANY Relationship
        amount = decimal.Decimal(0)
        for item in form['items']:
            orderitem = OrderItem(order = order, item = item)

            # Caculate amount
            orderitem.unit_amount = item.amount
            if 'orderitem_quantity' in form:
                orderitem.quantity = int(form['orderitem_quantity'])
            else :
                orderitem.quantity = 1
            orderitem.total_amount = orderitem.unit_amount * orderitem.quantity
            amount = amount +  orderitem.total_amount

            order.orderitems.append(orderitem)

        order.amount = amount
        db.session.add(order)
        db.session.commit()

    def update_data(self, some_id, form ):
        order = Order.query.get_or_404(some_id)

        order.status =form['status']

        order.user = form['user']

        order.is_active = form['is_active']


        # MANY-TO-MANY Relationship
        order.orderitems = []
        amount = decimal.Decimal(0)
        for item in form['items']:
            orderitem = OrderItem(item = item)

            # Caculate amount
            orderitem.unit_amount = item.amount
            if 'orderitem_quantity' in form:
                orderitem.quantity = int(form['orderitem_quantity'])
            else :
                orderitem.quantity = 1
            orderitem.total_amount = orderitem.unit_amount * orderitem.quantity
            amount = amount +  orderitem.total_amount

            order.orderitems.append(orderitem)
        
        order.amount = amount
        db.session.commit()

    def destroy_data(self, some_id ):
        order = Order.query.get_or_404(some_id)
        if order.status == 'cart' and session.get('order_id'):
            session.pop('order_id')
        db.session.delete(order)
        db.session.commit()


    def __repr__(self):
        # return '<User: {}>'.format(self.id)
        return '<Order %r>' % self.id


#######################
# WARNING FIXED ISSUE : OrderItem model registered at the end of this page to fixe issue  :  global name 'Order' is not defined
#######################

from app.modules.items.models import OrderItem