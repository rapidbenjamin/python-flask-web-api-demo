#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import datetime
import sendgrid
import os
import json
import decimal
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from flask import request, render_template, flash, current_app, g, redirect, abort, jsonify, url_for, session

from time import time
from flask_login import login_required, current_user

import paypalrestsdk as paypal
from paypalrestsdk import *

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app, logger
from app.modules.payments import payments_page
from app.modules.payments.models.payment_model import Payment
from app.modules.users.models import User
from app.helpers import *
from app.modules.localization.controllers import get_locale, get_timezone
from app import config_name
from app.modules.payments.constants import *
from app.modules.payments.forms.payment_form import *
from app.modules.orders.models import Order
from app.modules.payments.models.creditcard_model import Creditcard
from app.modules.payments.models.payment_model import Payment
from app import db



# -------  ROUTINGS AND METHODS  ------- 

# PAYPAL
paypal.configure({
    "mode": app.config['PAYPAL_MODE'],  # sandbox or live
    "client_id": app.config['PAYPAL_CLIENT_ID'],
    "client_secret": app.config['PAYPAL_CLIENT_SECRET']
})




# Payment checkout
@payments_page.route('/<int:id>/checkout/<int:order_id>', methods=['GET', 'POST'])
@payments_page.route('/checkout/<int:order_id>', methods=['GET', 'POST'])
def payment_checkout(id=None, order_id=None):
    try:

        # New payment
        if id :
            payment = Payment().read_data(id)
            order  = payment.order
        else :

            order = Order().read_data(order_id)
            payment = Payment(
                                status= 'new',
                                amount = decimal.Decimal(order.amount),
                                user = order.user,
                                order = order,
                                is_active = True
            )
            db.session.add(payment)
            db.session.commit()
        
        

        form = request.form

        # Process checkout
        if request.method == 'POST':
            
            

            # credit card payment mode
            # m_creditcard = CreditCard().read_data(form.creditcard.data)
            # payment.creditcard = m_creditcard.id
            # vv2 = form.vv2.data


            # paypal payment mode
            # A Payment Resource; create one using
            # the above types and intent as 'sale'
            paypal_payment = paypal.Payment({
                "intent": "sale",

                # Payer
                # A resource representing a Payer that funds a payment
                # Payment Method as 'paypal'
                "payer": {
                    "payment_method": "paypal"},

                # Redirect URLs
                "redirect_urls": {
                    "return_url": "http://%s/payments/%s/return/%s" %(app.config['APP_URL'], payment.id, order.id),
                    "cancel_url": "http://%s/payments/%s/checkout/%s" %(app.config['APP_URL'], payment.id, order.id)
                },

                # Transaction
                # A transaction defines the contract of a
                # payment - what is the payment for and who
                # is fulfilling it.
                "transactions": [{

                    # ItemList
                    "item_list": {
                        "items": [{
                            "name": "item",
                            "sku": "item",
                            "price": "%s" %(payment.amount),
                            "currency": "USD",
                            "quantity": 1}]
                    },

                    # Amount
                    # Let's you specify a payment amount.
                    "amount": {
                        "total": "%s" %(payment.amount),
                        "currency": "USD"},
                    "description": "test 123 This is the payment transaction description."}]})

            # Create Payment and return status
            if paypal_payment.create():
                print("Payment[%s] created successfully" % (paypal_payment.id))
                if request.is_xhr == True:
                    return jsonify(data = { message :"Payment[%s] created successfully" % (paypal_payment.id) }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Payment[%s] created successfully" % (paypal_payment.id), category="success")

                # Redirect the user to given approval url
                for link in paypal_payment.links:
                    if link.method == "REDIRECT":
                        # Convert to str to avoid google appengine unicode issue
                        # https://github.com/paypal/rest-api-sdk-python/pull/58
                        redirect_url = str(link.href)

                        if request.is_xhr == True:
                            return jsonify(data = { message :"Redirect for approval: %s" % (redirect_url)}), 200, {'Content-Type': 'application/json'}
                        else:
                            flash("Redirect for approval: %s" % (redirect_url), category="success")
                            return redirect(redirect_url)
            else:
  
                if request.is_xhr == True:
                    return jsonify(data = { message :"Error while creating payment"}), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Error while creating payment: %s" %(paypal_payment.error), category="danger")
        

        
        form.action = url_for('payments_page.payment_checkout', id=payment.id, order_id=order.id)


        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = payment)
        else:
            return render_template("payments/checkout.html", payment=payment, form=form, title_en_US='Checkout', app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)



# Payment return
@payments_page.route('/<int:id>/return/<int:order_id>', methods=['GET', 'POST'])
def payment_return(id=None, order_id=None):
    try:
        # ID of the payment. This ID is provided when creating payment.
        paypal_paymentId = request.args['paymentId']
        paypal_payer_id = request.args['PayerID']
        paypal_payment = paypal.Payment.find(paypal_paymentId)

        # PayerID is required to approve the payment.
        if paypal_payment.execute({"payer_id": paypal_payer_id}):  # return True or False

            # Update  payment and order
            payment = Payment().read_data(id)
            payment.status = "paid"
            payment.order.status = "paid"
            db.session.commit()
            if session.get('order_id'):
                session.pop('order_id')

            if request.is_xhr == True:
                return jsonify(data = { message :"Payment[%s] execute successfully" % (paypal_payment.id) }), 200, {'Content-Type': 'application/json'}
            else : 
                flash("Payment[%s] execute successfully" % (paypal_payment.id), category="success")
                return redirect(url_for('orders_page.show', id = order_id))

        else:
            flash(paypal_payment.error, category="error")
            return redirect(url_for('payments_page.checkout', id = id))

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)



# All payments
@payments_page.route('/')
@payments_page.route('/<int:page>')
def index(page=1):
    try:
        m_payments = Payment()
        list_payments = m_payments.all_data(page, app.config['LISTINGS_PER_PAGE'])
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = [{'id' : d.id, 'title_en_US' : d.title_en_US, 'description_en_US' : d.description_en_US, 'title_fr_FR' : d.title_fr_FR, 'description_fr_FR' : d.description_fr_FR} for d in list_payments.items])
        else:
            return render_template("payments/index.html", list_payments=list_payments, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        #abort(404)




# Show payment
@payments_page.route('/<int:id>/show')
def show(id=1):
    try:
        m_payments = Payment()
        m_payment = m_payments.read_data(id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = m_payment)
        else:
            return render_template("payments/show.html", payment=m_payment, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# New payment
@payments_page.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    try :

        form = Form_Record_Add(request.form)

        users = User.query.filter(User.is_active == True).all()
        orders = Order.query.filter(Order.is_active == True).all()
        creditcards = Creditcard.query.filter(Creditcard.is_active == True).all()

        if request.method == 'POST':

            if form.validate():

                payments = Payment()

                sanitize_form = {

                    'status' : form.status.data,

                    'key_id' : form.key_id.data,

                    'amount' : form.amount.data,

                    'user' : form.user.data,

                    'order' : form.order.data,

                    'creditcard' : form.creditcard.data,

                    'params' : form.params.data,

                    'comments' : form.comments.data,

                    'is_active' : form.is_active.data
                }

                payments.create_data(sanitize_form)
                logger.info("Adding a new record.")
                
                if request.is_xhr == True:
                    return jsonify(data = { message :"Record added successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record added successfully.", category="success")
                    return redirect("/payments")

        form.action = url_for('payments_page.new')

         # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("payments/edit.html", form=form,  creditcards = creditcards, orders = orders, users = users, title_en_US='New', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# Edit payment
@payments_page.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id=1):
    try : 

        # check_admin()

        payments = Payment()
        payment = payments.query.get_or_404(id)

        # users = User.query.all()
        users = User.query.filter(User.is_active == True).all()
        orders = Order.query.filter(Order.is_active == True).all()
        creditcards = Creditcard.query.filter(Creditcard.is_active == True).all()

        # request.form only contains form input data. request.files contains file upload data. 
        # You need to pass the combination of both to the form. 
        form = Form_Record_Add(request.form)

        if request.method == 'POST':
            if form.validate():

                sanitize_form = {

                    'status' : form.status.data,

                    'key_id' : form.key_id.data,

                    'amount' : form.amount.data,

                    'user' : form.user.data,

                    'order' : form.order.data,

                    'creditcard' : form.creditcard.data,

                    'params' : form.params.data,

                    'comments' : form.comments.data,

                    'is_active' : form.is_active.data
                }

                payments.update_data(payment.id, sanitize_form)

                # Remove current payment
                #if payment.status != 'cart' and session.get('payment_id'):
                    #session.pop('payment_id')

                logger.info("Editing a new record.")
                
                if request.is_xhr == True:
                    return jsonify(data = { message :"Record updated successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                else : 
                    flash("Record updated successfully.", category="success")
                    return redirect("/payments")

        form.action = url_for('payments_page.edit', id = payment.id)

        form.status.data = payment.status

        form.key_id.data = payment.key_id

        if  payment.user :
            form.user.data = payment.user.id

        if  payment.order :
            form.order.data = payment.order.id

        if  payment.creditcard :
            form.creditcard.data = payment.creditcard.id
        
        form.params.data = payment.params
        form.comments.data = payment.comments

        form.is_active.data = payment.is_active

        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("payments/edit.html", form=form,   creditcards = creditcards, orders = orders, users = users, title_en_US='Edit', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)



# Delete payment
@payments_page.route('/<int:id>/destroy')
@login_required
def destroy(id=1):
    try:
        payments = Payment()
        payment = payments.query.get_or_404(id)

        payments.destroy_data(payment.id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = {message:"Record deleted successfully.", payment : m_payment})
        else:
            flash("Record deleted successfully.", category="success")
            return redirect(url_for('payments_page.index'))

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)