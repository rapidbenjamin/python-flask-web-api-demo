#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import datetime
from sqlalchemy import desc
from sqlalchemy import or_


from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# ------- IMPORT LOCAL DEPENDENCIES  -------
from ... import db


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
    # one-to-many relationship with the Group model
    group_id = db.Column(db.Integer, db.ForeignKey('Groups.id'))
    # Flask_login requirements

    # is_authenticated usually returns True. 
    # This should return False only in cases where we do not want a user to be authenticated. 
    is_authenticated = db.Column(db.Boolean, default=True)

    # is_active usually returns True. 
    # This should return False only in cases where we have blocked or banned a user. 
    is_active = db.Column(db.Boolean, default=True)

    # is_anonymous is used to indicate a user who is not supposed to be logged in to the system and should access the application as anonymous. 
    # This should usually return False for regular logged-in users.
    is_anonymous = db.Column(db.Boolean, default=False) 

    is_admin = db.Column(db.Boolean, default=False)
    is_editor = db.Column(db.Boolean, default=False)
    is_member = db.Column(db.Boolean, default=False)
    added_time = db.Column(db.DateTime, default=datetime.datetime.now)

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


    def get_user(self, some_id):
        user = Users.query.filter(Users.id == some_id).first_or_404()
        return user


    def add_data(self, form):
        user = Users(email=form['email'], username=form['username'])
        db.session.add(user)
        db.session.commit()


    def list_all(self, page, LISTINGS_PER_PAGE):
        return Users.query.order_by(desc(Users.added_time)).paginate(page, LISTINGS_PER_PAGE, False)

    
    def update_data(self, some_id, form ):
        user = Users.query.get_or_404(some_id)

        user.email = form['email']
        user.username = form['username']

        db.session.commit()

    def delete_data(self, some_id ):
        user = Users.query.get_or_404(some_id)
        db.session.delete(user)
        db.session.commit()


    def __repr__(self):
        return '<Users: {}>'.format(self.id)




