from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, ValidationError
from wtforms.fields.core import DateField, FieldList, FormField, SelectField, TimeField
from wtforms.fields.simple import TextAreaField
from wtforms.fields.html5 import DateField as DateFieldHTML5
from wtforms.fields.html5 import TimeField as TimeFieldHTML5
from wtforms.validators import DataRequired, Length, Email, ValidationError
from datetime import datetime

from mss.User.UserModels import Client


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
    end_time = SelectField('End Time', coerce=str)
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

class AdminSelectMeetingByTime(FlaskForm):
    dt_start_date = DateFieldHTML5('Start Date', format='%Y-%m-%d', default=datetime.now(),
                                   validators=[DataRequired()])
    dt_start_time = TimeFieldHTML5('Start Time', format='%H:%M', default=datetime.now(),
                                   validators=[DataRequired()])
    dt_end_date = DateFieldHTML5('End Date', format='%Y-%m-%d', default=datetime.now(),
                                 validators=[DataRequired()])
    dt_end_time = TimeFieldHTML5('End Time', format='%H:%M', default=datetime.now(),
                                 validators=[DataRequired()])