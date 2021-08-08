from wtforms.fields.html5 import DateField as DateFieldHTML5
from wtforms.fields.html5 import TimeField as TimeFieldHTML5
from flask_wtf import FlaskForm, Form
from datetime import datetime
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import ValidationError
from wtforms import validators
from wtforms.fields.core import DateField, FieldList, FormField, SelectField, TimeField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError

from mss.models import User, Client, Room
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

class ParticipantForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    def validate_email(self, email):
        client = Client.query.filter_by(email=email.data).first()
        
        if not client:
            raise ValidationError('Participant must have an account!')

        if current_user.email == client.email:
            raise ValidationError('Cant invite yourself!')

class CreateMeetingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=120)])
    date = DateField('Date', format='%m/%d/%y', validators=[DataRequired()])
    start_time = SelectField('Start Time', coerce=str)
    end_time =  SelectField('End Time',  coerce=str)
    description = TextAreaField('Description')
    room = SelectField('Room', coerce=int)
    participants = FieldList(FormField(ParticipantForm), min_entries=1)

    submit = SubmitField('Submit')

    # custom validation
    def validate_end_time(self, end_time):
        start = datetime.strptime(self.start_time.data, '%I:%M %p')
        end = datetime.strptime(self.end_time.data, '%I:%M %p')

        if start >= end:
            raise ValidationError('End time must be after start time')


class UpdateUserBill(FlaskForm):
    client_id = StringField('Client ID', validators=[DataRequired(), Length(max=20)])
    total = StringField('Update Total', validators=[DataRequired(), Length(max=20)])
    date = StringField('Update Due Date', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Submit Billing Changes')


class AdminSelectMeeting(FlaskForm):
    select_meeting = SelectField('Please Select Meetings to Display', coerce=str)
    submit = SubmitField('Display Meetings')


class AdminSelectMeetingByWeek(FlaskForm):
    dt = DateFieldHTML5('DatePicker', format='%Y-%m-%d', default=datetime.now(), validators=[DataRequired()])


class AdminSelectMeetingByDay(FlaskForm):
    dt = DateFieldHTML5('DatePicker', format='%Y-%m-%d', default=datetime.now(), validators=[DataRequired()])


def roomQuery():
    return Room.query


class AdminSelectMeetingByRoom(FlaskForm):
    select_room = QuerySelectField(query_factory=roomQuery, allow_blank=True)


def userQuery():
    return User.query


class AdminSelectMeetingByPerson(FlaskForm):
    select_person = QuerySelectField(query_factory=userQuery, allow_blank=True)


class AdminSelectMeetingByTime(FlaskForm):
    dt_start_date = DateFieldHTML5('Start Date', format='%Y-%m-%d', default=datetime.now(),
                                   validators=[DataRequired()])
    dt_start_time = TimeFieldHTML5('Start Time', format='%H:%M', default=datetime.now(),
                                   validators=[DataRequired()])
    dt_end_date = DateFieldHTML5('End Date', format='%Y-%m-%d', default=datetime.now(),
                                 validators=[DataRequired()])
    dt_end_time = TimeFieldHTML5('End Time', format='%H:%M', default=datetime.now(),
                                 validators=[DataRequired()])
