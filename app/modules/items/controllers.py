#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import datetime
import decimal
import sendgrid
from sqlalchemy import desc
from sqlalchemy import or_, and_
from flask import request, render_template, flash, current_app, redirect, abort, jsonify, url_for
from forms import *
from time import time
from flask_login import login_required, current_user


# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app, logger
from . import items_page
from models import Item
from app.helpers import *
from app.modules.localization.controllers import get_locale, get_timezone

from app.modules.sections.models import Section
from app.modules.assets.models import Asset
from app.modules.orders.models import Order
from app.modules.users.models import User


# -------  ROUTINGS AND METHODS  ------- 



# All items
@items_page.route('/', methods=['GET','POST'])
@items_page.route('/<int:page>', methods=['GET','POST'])
def index(page=1):
    try:
        
        users = User.query.filter(User.is_active == True).all()
        sections = Section.query.filter(Section.is_active == True).all()


        m_items = Item()
        list_items = m_items.all_data(page, app.config['LISTINGS_PER_PAGE'])

        # if request.args and 'item_keyword' in request.args:
        if request.method == 'POST' and (request.form['item_userid'] or request.form['item_sectionid'] or request.form['item_keyword']):   
            filter_items = Item.query
            # list_items = Item.query.filter(Item.slug == request.args['item_keyword']).order_by(desc(Item.created_at)).paginate(page, LISTINGS_PER_PAGE, False)
            if request.form['item_userid'] != "":
                filter_items = filter_items.filter(  Item.user_id.in_(request.form['item_userid']))
            if request.form['item_sectionid'] != "":
                filter_items = filter_items.filter(Item.sections.any(Section.id.in_(request.form['item_sectionid'])))
            if request.form['item_keyword'] != "":
                filter_items = filter_items.filter(or_(Item.slug.like("%"+request.form['item_keyword']+"%"), Item.title_en_US.like("%"+request.form['item_keyword']+"%"), Item.description_en_US.like("%"+request.form['item_keyword']+"%")))
            # list_items = list_items.filter(Item.user_id = request.form['item_user'])

            list_items = filter_items.order_by(desc(Item.created_at)).paginate(page, app.config['LISTINGS_PER_PAGE'], False)
        
        # html or Json response
        if request_wants_json():
            return jsonify([{'id' : d.id, 'title_en_US' : d.title_en_US, 'description_en_US' : d.description_en_US, 'title_fr_FR' : d.title_fr_FR, 'description_fr_FR' : d.description_fr_FR} for d in list_items.items])
        else:
            return render_template("items/index.html", sections = sections, users = users, list_items=list_items, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        #abort(404)


# Show item
@items_page.route('/<int:id>/show', methods=['GET','POST'])
def show(id=1):
    try:
        m_items = Item()
        m_item = m_items.read_data(id)
        # html or Json response
        if request_wants_json():
            return jsonify(data = m_item)
        else:
            return render_template("items/show.html", item=m_item, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# New item
@items_page.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    try :

        sections = Section.query.filter(Section.is_active == True).all()
        assets = Asset.query.filter(Asset.is_active == True).all()
        orders = Order.query.filter(Order.is_active == True).all()
        users = User.query.filter(User.is_active == True).all()

        form = Form_Record_Add(request.form)

        if request.method == 'POST':
            if form.validate():
                items = Item()

                sanitize_form = {

                    'slug' : form.slug.data,

                    'type' : form.type.data,

                    'title_en_US' : form.title_en_US.data,
                    'title_fr_FR' : form.title_fr_FR.data,

                    'description_en_US' : sanitize_html(form.description_en_US.data),
                    'description_fr_FR' : sanitize_html(form.description_fr_FR.data),

                    'amount' : decimal.Decimal(form.amount.data),

                    'user' : form.user.data,

                    'sections' : form.sections.data,

                    'assets' : form.assets.data,

                    'orders' : form.orders.data,


                    'is_active' : form.is_active.data
                }

                items.create_data(sanitize_form)
                logger.info("Adding a new record.")
                
                if request_wants_json():
                    return jsonify(data = { message :"Record added successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record added successfully.", category="success")
                    return redirect("/items")

        form.action = url_for('items_page.new')

         # html or Json response
        if request_wants_json():
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("items/edit.html", form=form, sections=sections, users = users, assets=assets, orders=orders,  title_en_US='New', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# Edit item
@items_page.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id=1):
    try : 

        # check_admin()
        
        sections = Section.query.filter(Section.is_active == True).all()
        assets = Asset.query.filter(Asset.is_active == True).all()
        orders = Order.query.filter(Order.is_active == True).all()
        # users = User.query.all()
        users = User.query.filter(User.is_active == True).all()


        items = Item()
        item = Item.query.get_or_404(id)

        form = Form_Record_Add(request.form)

        if request.method == 'POST':
            if form.validate():

                sanitize_form = {
                    'slug' : form.slug.data,

                    'type' : form.type.data,

                    'title_en_US' : form.title_en_US.data,
                    'title_fr_FR' : form.title_fr_FR.data,

                    'description_en_US' : sanitize_html(form.description_en_US.data),
                    'description_fr_FR' : sanitize_html(form.description_fr_FR.data),

                    'amount' : decimal.Decimal(form.amount.data),

                    'user' : form.user.data,

                    'sections' : form.sections.data,
                    'assets' : form.assets.data,
                    'orders' : form.orders.data,


                    'is_active' : form.is_active.data
                }

                items.update_data(item.id, sanitize_form)
                logger.info("Editing a new record.")
                
                if request_wants_json():
                    return jsonify(data = { message :"Record updated successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record updated successfully.", category="success")
                    return redirect("/items")

        form.action = url_for('items_page.edit', id = item.id)

        form.slug.data = item.slug

        form.type.data = item.type

        form.title_en_US.data = item.title_en_US
        form.title_fr_FR.data = item.title_fr_FR

        form.description_en_US.data = item.description_en_US
        form.description_fr_FR.data = item.description_fr_FR

        form.amount.data = item.amount

        if  item.user :
            form.user.data = item.user.id

        if  item.sections :
            form.sections.data = item.sections

        if  item.assets :
            form.assets.data = item.assets

        if  item.orders :
            form.orders.data = item.orders


        form.is_active.data = item.is_active

        # html or Json response
        if request_wants_json():
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("items/edit.html", form=form, users = users, sections=sections, assets=assets, orders=orders, title_en_US='Edit', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)



# Delete item
@items_page.route('/<int:id>/destroy')
@login_required
def destroy(id=1):
    try:
        items = Item()
        item = items.query.get_or_404(id)
        items.destroy_data(item.id)
        # html or Json response
        if request_wants_json():
            return jsonify(data = {message:"Record deleted successfully.", item : m_item})
        else:
            flash("Record deleted successfully.", category="success")
            return redirect(url_for('items_page.index'))

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)