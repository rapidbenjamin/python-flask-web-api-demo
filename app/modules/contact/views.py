#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
from flask import request, render_template, flash, current_app, redirect, abort, jsonify
import sendgrid

# ------- IMPORT LOCAL DEPENDENCIES  -------
from . import contact_page
from app import app
from app.helpers import threaded_async



# SERVICE EMAIL
@threaded_async
def send_email(app, to, subject, body):
    with app.app_context():
        sg = sendgrid.SendGridClient("SG.pRFA8c9bRXXXXXXXXXXXXXXXXXXXXXXXXX")
        message = sendgrid.Mail()
        message.add_to(to)
        message.set_subject(subject)
        message.set_html(body)
        message.set_from('Template No-Reply <noreply@example.com>')
        try:
            status, msg = sg.send(message)
            print("Status: " + str(status) + " Message: " + str(msg))
            if status == 200:
                return True
        except Exception, ex:
            print("------------ ERROR SENDING EMAIL ------------" + str(ex.message))
    return False

# CONTACT PAGE
@contact_page.route('/', methods=['GET', 'POST'])
def index():
    try:
        recaptcha = current_app.config['RECAPTCHA_SITE_KEY']
        email_sent = False
        post = { 'title' : 'Contact page' , 'description' : 'contact page' }


        if request.method == 'POST':
            email = request.form['email']
            name = request.form['name']
            message = request.form['message']
            recaptcha_response = request.form['g-recaptcha-response']

            send_email(app, to=current_app.config['ADMIN_EMAIL'], subject="Contact Form Flask Shop",
                    body=email + " " + name + " " + message)

            email_sent = True


        # html or Json response
        if request.is_xhr == True :
            return jsonify(data = post), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("contact/contact.html", RECAPTCHA_SITE_KEY=recaptcha, email_sent=email_sent, post = post, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        return render_template('404.html', post = {'title' : 'Error' , 'description' : str(ex.message) }, app = app )
        #abort(404)