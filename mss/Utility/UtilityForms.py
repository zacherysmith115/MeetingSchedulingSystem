from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import SelectField
from wtforms.fields.html5 import DateField as DateFieldHTML5
from wtforms.fields.html5 import TimeField as TimeFieldHTML5
from wtforms.validators import DataRequired, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from datetime import datetime

from mss.User.UserModels import Client
from mss.Meeting.MeetingModels import Room


# Factory method needed for QuerySelectField
def clientQuery():
    return Client.query

# Factory method needed for QuerySelectField
def roomQuery():
    return Room.query


# Form to update user billing information
class UpdateUserBill(FlaskForm):
    client_id = QuerySelectField(query_factory=clientQuery, allow_blank=False)
    total = StringField('Update Total:', validators=[DataRequired(), Length(max=20)])
    date = StringField('Update Due Date:', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Submit Billing Changes')


# Form to provide a display method for an admin
class AdminSelectMeeting(FlaskForm):
    select_meeting = SelectField('Please Select Meetings to Display', 
            choices = [(1, 'By Week'), (2, 'By Day'), (3, 'By Room'), (4, 'By Person'), (5, 'By Time Slot')],
            default = 1)

    submit = SubmitField('Display Meetings')


# Form to get a given date to display meetings by week
class AdminSelectMeetingByDay(FlaskForm):
    dt = DateFieldHTML5('Select Date:', format='%Y-%m-%d', default=datetime.now(), validators=[DataRequired()])
    submit = SubmitField('Submit')

# Form to get a selected room
class AdminSelectMeetingByRoom(FlaskForm):
    select_room = QuerySelectField('Select Room:', query_factory=roomQuery, allow_blank=False)
    submit = SubmitField('Submit')


# Form to get a selected client
class AdminSelectMeetingByPerson(FlaskForm):
    select_person = QuerySelectField(query_factory=clientQuery, allow_blank=False)
    submit = SubmitField('Submit')


# Form to get two given points in time
class AdminSelectMeetingByTime(FlaskForm):
    dt_start_date = DateFieldHTML5('Start Date:', format='%Y-%m-%d', default=datetime.now(), validators=[DataRequired()])
    dt_start_time = TimeFieldHTML5('Start Time:', format='%H:%M', default=datetime.now(), validators=[DataRequired()])
    dt_end_date = DateFieldHTML5('End Date:', format='%Y-%m-%d', default=datetime.now(), validators=[DataRequired()])
    dt_end_time = TimeFieldHTML5('End Time:', format='%H:%M', default=datetime.now(), validators=[DataRequired()])
    submit = SubmitField('Submit')


