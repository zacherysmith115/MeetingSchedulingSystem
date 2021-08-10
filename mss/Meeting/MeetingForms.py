from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, ValidationError
from wtforms.fields.core import FieldList, FormField
from wtforms.fields.simple import TextAreaField
from wtforms.fields.html5 import DateField as DateFieldHTML5
from wtforms.fields.html5 import TimeField as TimeFieldHTML5
from wtforms.validators import DataRequired, Length, Email, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from datetime import datetime

from mss.User.UserModels import Client
from mss.Utility.UtilityForms import roomQuery


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
    date = DateFieldHTML5('Date', format='%Y-%m-%d', default=datetime.now(), validators=[DataRequired()])

    start_time = TimeFieldHTML5('Start Time', format='%H:%M', default=datetime.now(), validators=[DataRequired()])
    end_time = TimeFieldHTML5('End Time', format='%H:%M', default=datetime.now(), validators=[DataRequired()])
    description = TextAreaField('Description')

    room = QuerySelectField('Select Room:', query_factory=roomQuery, allow_blank=False)
    participants = FieldList(FormField(ParticipantForm), min_entries=1)

    submit = SubmitField('Submit')

    # Ensure end time is later than start time
    def validate_end_time(self, end_time):
        if self.start_time.data >= self.end_time.data:
            raise ValidationError('End time must be after start time')

    # Ensure room is available 
    def validate_room(self, room):

         # build datetime 
        start_time = datetime.combine(self.date.data, self.start_time.data)
        end_time = datetime.combine(self.date.data, self.end_time.data)

        for meeting in room.data.meetings:
            print(meeting)
            if meeting.start_time < start_time < meeting.end_time or meeting.start_time < end_time < meeting.end_time or meeting.start_time == start_time:
                tstr1 = meeting.start_time.time().strftime("%I:%M %p")
                tstr2 = meeting.end_time.time().strftime("%I:%M %p")
                raise ValidationError("Room unavaible from "  + tstr1 + " to " + tstr2)
            

    # Ensure nobody has a conflicting schedule 
    def validate_participants(self, participants):
        
        flag = False

        for entry in participants.entries:
            client = Client.query.filter_by(email=entry.email.data).first()

            from mss.Meeting.MeetingController import MeetingController
            controller = MeetingController()

            meetings = controller.buildMeeetingListParticipant(client)
            meetings.extend(controller.buildMeetingListCreator(client))

            for meeting in meetings:

                # build datetime 
                start_time = datetime.combine(self.date.data, self.start_time.data)
                end_time = datetime.combine(self.date.data, self.end_time.data)

                if meeting.start_time < start_time < meeting.end_time or meeting.start_time < end_time < meeting.end_time:
                    entry.email.errors.append(ValidationError('Participtant: ' + client.email + ' has a conflicting schedule.'))
                    flag = True
        
        if flag:
            raise ValidationError()
            



class AdminSelectMeetingByTime(FlaskForm):
    dt_start_date = DateFieldHTML5('Start Date', format='%Y-%m-%d', default=datetime.now(),
                                   validators=[DataRequired()])
    dt_start_time = TimeFieldHTML5('Start Time', format='%H:%M', default=datetime.now(),
                                   validators=[DataRequired()])
    dt_end_date = DateFieldHTML5('End Date', format='%Y-%m-%d', default=datetime.now(),
                                 validators=[DataRequired()])
    dt_end_time = TimeFieldHTML5('End Time', format='%H:%M', default=datetime.now(),
                                 validators=[DataRequired()])