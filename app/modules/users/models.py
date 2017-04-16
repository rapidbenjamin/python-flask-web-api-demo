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
from app import db
from app.helpers import *
from app.modules.localization.controllers import get_locale, get_timezone
# from app.modules.assets.models import Asset


# from app.modules.sections.models import Section
# from app.modules.sections.models import UserSection

#######################
# WARNING FIXED ISSUE : UserSection model registered at the end of this page to fixe issue  :  global name 'User' is not defined
#######################


class User(UserMixin, db.Model):
    """
    Create a User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # one-to-many relationship with the Asset model
    assets = db.relationship('Asset', back_populates='user')

    # MANY-TO-MANY relationship with EXTRA_DATA columns association and the Section model
    # the cascade will delete orphaned usersections
    usersections = db.relationship('UserSection', back_populates='user', lazy='dynamic',  cascade="all, delete-orphan")
    # or  Get all sections in view only mode
    sections = db.relationship('Section', secondary='usersection', viewonly=True, back_populates='users', lazy='dynamic')

    """
    Return UserSection objects collection
    and requires that child objects are associated with an association instance before being appended to the parent;
    similarly, access from parent to child goes through the association object:
    so to append sections via association
        user1.usersections.append(UserSection(section = Section(title_en_US = 'test')))

    or
        UserSection(user = user1, Section(title_en_US = 'test'), extra_data="test")
    To iterate through sections objects via association, including association attributes
        for usersection in user.usersections:
            print(usersection.extra_data)
            print(usersection.section)
        or 
        for section in user.sections:
            print(section.title_en_US)
    WARNING : So don't use  directly user.sections.append(Section(title_en_US = 'test'))
                cause it's redundant, it will cause a duplicate INSERT on Association with 
                user.usersections.append(UserSection(section=section1))
                add  viewonly=True on secondary relationship to stop edit, create or delete operations  here
    """


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
        return User.query.order_by(desc(User.created_at)).paginate(page, LISTINGS_PER_PAGE, False)

    def read_data(self, some_id):
        user = User.query.filter(User.id == some_id).first_or_404()
        return user


    def create_data(self, form):
        
        # dateTime conversion to timestamp
        timestamp_created_at = string_datetime_utc_to_string_timestamp_utc(form['created_at'])


        user = User(
                        email=form['email'], 
                        username=form['username'],
                        
                        is_active = form['is_active'],
                        # convert string to integer format
                        created_at = int(timestamp_created_at)
                    )
                    
        # MANY-TO-MANY Relationship 
        for section in form['sections']:
            usersection = UserSection(user = user, section = section)
            user.usersections.append(usersection)
        
        db.session.add(user)
        db.session.commit()


    def update_data(self, some_id, form ):
        user = User.query.get_or_404(some_id)

        user.email = form['email']
        user.username = form['username']
        
        user.is_active = form['is_active']

        # dateTime conversion to timestamp
        timestamp_created_at = string_datetime_utc_to_string_timestamp_utc(form['created_at'])
        # convert string to integer format
        user.created_at = int(timestamp_created_at)

        # MANY-TO-MANY Relationship
        user.usersections = []
        for section in form['sections']:
            usersection = UserSection(section = section)
            user.usersections.append(usersection)


        db.session.commit()

    def destroy_data(self, some_id ):
        user = User.query.get_or_404(some_id)
        db.session.delete(user)
        db.session.commit()


    def __repr__(self):
        # return '<User: {}>'.format(self.id)
        return '<User %r>' % self.id


#######################
# WARNING FIXED ISSUE : UserSection model registered at the end of this page to fixe issue  :  global name 'User' is not defined
#######################

from app.modules.sections.models import UserSection