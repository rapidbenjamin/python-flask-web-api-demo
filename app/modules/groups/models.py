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
    users = db.relationship('Users', backref='group', lazy='dynamic')

    added_time = db.Column(db.DateTime, default=datetime.datetime.now)

    def list_all(self, page, LISTINGS_PER_PAGE):
        return Groups.query.order_by(desc(Groups.added_time)).paginate(page, LISTINGS_PER_PAGE, False)

    def get_group(self, some_id):
        group = Groups.query.filter(Groups.id == some_id).first_or_404()
        return group


    def add_data(self, form):
        new_record = Groups(title=form['title'], description=form['description'])
        db.session.add(new_record)
        db.session.commit()
    
    def update_data(self, some_id, form ):
        group = Groups.query.get_or_404(some_id)

        group.title = form['title']
        group.description = form['description']

        db.session.commit()

    def delete_data(self, some_id ):
        group = Groups.query.get_or_404(some_id)
        db.session.delete(group)
        db.session.commit()


    def __repr__(self):
        # return '<Users: {}>'.format(self.id)
        return '<Groups %r>' % self.id
