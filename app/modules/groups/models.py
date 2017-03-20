#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import datetime
from sqlalchemy import desc
from sqlalchemy import or_

# ------- IMPORT LOCAL DEPENDENCIES  -------
from ... import db
# from app.modules.users.models import Users


class Groups(db.Model):
    __tablename__ = "Groups"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text())
    # one-to-many relationship with the User model
    # lazy defines how the data will be loaded from the database; 
    # in this case it will be loaded dynamically, which is ideal for managing large collections.
    users = db.relationship('Users', backref='Group', lazy='dynamic')
    added_time = db.Column(db.DateTime, default=datetime.datetime.now)

    def get_id(self, some_id):
        record = Groups.query.filter(Groups.id == some_id).first_or_404()
        group = dict()
        group['id'] = record.id
        group['title'] = record.title
        group['description'] = record.description
        group['added_time'] = record.added_time
        return group


    def add_data(self, title, description):
        new_record = Groups(title=title, description=description)
        db.session.add(new_record)
        db.session.commit()


    def list_all(self, page, LISTINGS_PER_PAGE):
        return Groups.query.order_by(desc(Groups.added_time)).paginate(page, LISTINGS_PER_PAGE, False)


    # ------ Delete them if you don't plan to use them ----------

    def __str__(self):
        return '<Groups %r, %s>' % (self.id, self.title)
