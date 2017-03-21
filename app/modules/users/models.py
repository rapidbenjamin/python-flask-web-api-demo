#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import datetime
from sqlalchemy import desc
from sqlalchemy import or_

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# ------- IMPORT LOCAL DEPENDENCIES  -------
from ... import db,  login_manager


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
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    # one-to-many relationship with the Group model
    group_id = db.Column(db.Integer, db.ForeignKey('Groups.id'))
    # Flask_login requirements
    is_authenticated = db.Column(db.Boolean, default=False)    
    is_active = db.Column(db.Boolean, default=False)
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
    
    
    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        with Werkzeug's handy security helper method check_password_hash
        """
        return check_password_hash(self.password_hash, password)

    def get_id(self, some_id):
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

# Set user_loader callback for session management 
# which Flask-Login uses to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    # return Users.query.filter(Users.id == user_id)
    return Users.query.get(int(user_id))

