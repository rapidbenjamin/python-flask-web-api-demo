#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import datetime
from sqlalchemy import desc
from sqlalchemy import or_
import time

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# ------- IMPORT LOCAL DEPENDENCIES  -------
from ... import db
from app.helpers import *
from app.modules.localization.controllers import get_locale, get_timezone
from app.modules.sections.models import Sections
from app.modules.assets.models import Assets

class Users(UserMixin, db.Model):
    """
    Create a Users table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    # one-to-many relationship with the Asset model
    # the backref argument in the asset field allows us to access users from the Assets model 
    # as simple as asset.users in our controllers.
    asset_id = db.Column(db.Integer, db.ForeignKey('Assets.id'))
    # asset = db.relationship('Assets', backref=db.backref('users', lazy='dynamic'))


    is_admin = db.Column(db.Boolean, default=True)
    is_owner = db.Column(db.Boolean, default=False)
    is_member = db.Column(db.Boolean, default=True)

    # Flask_login requirements

    # is_authenticated usually returns True. 
    # This should return False only in cases where we do not want a user to be authenticated. 
    is_authenticated = db.Column(db.Boolean, default=True)

    # is_anonymous is used to indicate a user who is not supposed to be logged in to the system and should access the application as anonymous. 
    # This should usually return False for regular logged-in users.
    is_anonymous = db.Column(db.Boolean, default=False) 

    # is_active usually returns True. 
    # This should return False only in cases where we have blocked or banned a user. 
    is_active = db.Column(db.Boolean, index=True, default=True)

    updated_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()), onupdate=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    created_at = db.Column(db.Integer, default=string_datetime_utc_to_string_timestamp_utc(datetime.utcnow()))
    # updated_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple()), onupdate=time.mktime(datetime.utcnow().timetuple())) 
    # created_at = db.Column(db.Integer, default=time.mktime(datetime.utcnow().timetuple())) 

    locale = db.Column(db.String(30), index=True, default='en_US')
    timezone = db.Column(db.String(60), index=True, default='UTC')

    @property
    def password(self):
        """
        Prevent pasword from being accessed instead an error will be raised
        """
        raise AttributeError('password is not a readable attribute.')
    

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        with Werkzeug's handy security helper method generate_password_hash
        """
        self.password_hash = generate_password_hash(password)
    
    
    def check_password(self, password):
        """
        Check if hashed password matches actual password
        with Werkzeug's handy security helper method check_password_hash
        """
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """
        Get id in unicode format for flask login
        """
        return unicode(self.id)


    def all_data(self, page, LISTINGS_PER_PAGE):
        return Users.query.order_by(desc(Users.created_at)).paginate(page, LISTINGS_PER_PAGE, False)

    def read_data(self, some_id):
        user = Users.query.filter(Users.id == some_id).first_or_404()
        return user


    def create_data(self, form):
        
        # dateTime conversion to timestamp
        timestamp_created_at = string_datetime_utc_to_string_timestamp_utc(form['created_at'])

        user = Users(
                        email=form['email'], 
                        username=form['username'], 
                        asset = form['asset'], 
                        is_active = form['is_active'],
                        # convert string to integer format
                        created_at = int(timestamp_created_at)
                    )
        db.session.add(user)
        db.session.commit()


    def update_data(self, some_id, form ):
        user = Users.query.get_or_404(some_id)

        user.email = form['email']
        user.username = form['username']
        user.asset = form['asset']
        user.is_active = form['is_active']

        # dateTime conversion to timestamp
        timestamp_created_at = string_datetime_utc_to_string_timestamp_utc(form['created_at'])
        # convert string to integer format
        user.created_at = int(timestamp_created_at)

        db.session.commit()

    def destroy_data(self, some_id ):
        user = Users.query.get_or_404(some_id)
        db.session.delete(user)
        db.session.commit()


    def __repr__(self):
        # return '<Users: {}>'.format(self.id)
        return '<Users %r>' % self.id




