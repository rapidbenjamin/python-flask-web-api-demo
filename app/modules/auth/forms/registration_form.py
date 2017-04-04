#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
import base64

from app.modules.users.models import Users


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """



    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    
    # use the EqualTo validator to confirm that the password and confirm_password fields match 
    password = PasswordField('Password', validators=[
                                                    DataRequired(),
                                                    EqualTo('confirm_password')
                                                    ])
    confirm_password = PasswordField('Confirm Password')

    submit = SubmitField('Register')

    # Method to ensure that the email entered have not been used before
    def validate_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')
    
    # Method to ensure that the username entered have not been used before
    def validate_username(self, field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')
    
