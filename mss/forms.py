import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import ValidationError
from wtforms.fields.core import DateField, SelectField, TimeField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from mss.models import User
from mss import app, db
from sqlalchemy import inspect


# Contains all the forms to dynamically server to the browser #

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CreateAccountForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=60)])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Create Account')

    # custom validation
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Account already created')


class EditAccountForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=60)])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Save Changes')


class PaymentInfoForm(FlaskForm):
    card_name = StringField('Name on Card', validators=[DataRequired(), Length(max=40)])
    card_number = StringField('Card Number', validators=[Length(min=16, max=16)])
    card_exp_date = StringField('Card Expiration Date (MM/YY)', validators=[Length(min=5, max=5)])
    card_ccv = PasswordField('CCV', validators=[Length(min=3, max=4)])

    submit = SubmitField('Save Changes')


class DelRoomForm(FlaskForm):
    del_room = StringField('Delete Room', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Delete Room Submit')


class AddRoomForm(FlaskForm):
    add_room = StringField('Add Room', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Add Room Submit')

class CreateMeetingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=120)])
    date = DateField('Date', format ='%m/%d/%y',validators=[DataRequired()])
    start_time = SelectField('Start Time', coerce=str)
    end_time =  SelectField('End Time', coerce=str)
    description = TextAreaField('Description')

    submit = SubmitField('Submit')

class UpdateUserBill(FlaskForm):
    client_id = StringField('Client ID', validators=[DataRequired(), Length(max=20)])
    total = StringField('Update Total', validators=[DataRequired(), Length(max=20)])
    date = StringField('Update Due Date', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Submit Billing Changes')

