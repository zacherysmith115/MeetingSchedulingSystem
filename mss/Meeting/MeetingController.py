from datetime import timedelta, datetime
from sqlalchemy.sql.elements import and_
from sqlalchemy.orm.collections import InstrumentedList

from mss.Meeting.MeetingModels import Meeting, Room
from mss.User.UserModels import Client
from mss.Utility.UtilityController import UtilityController
from mss.Meeting.MeetingForms import CreateMeetingForm


class MeetingController:
    db = None

    def __init__(self) -> None:
        self.db = __import__('mss').db

    # Function to provide meetings between a given date and time delta
    def getMeetingsInDelta(self, delta: "timedelta", date: "str") -> list:
        end_time = datetime.strptime(date, '%Y-%m-%d') + delta
        return Meeting.query.filter(and_(Meeting.start_time >= date, Meeting.start_time <= end_time))

    # Function add a room 
    def addRoom(self, id: "int", is_special: "bool") -> bool:

        # Check room doesnt exist
        if Room.query.filter_by(id=id).first() is None:
            room = Room(id=id)

            if is_special:
                room.special = True
                room.cost = 100
            try:
                self.db.session.add(room)
                self.db.session.commit()
                return True

            except:
                return False

        return False

    # Function remove a room
    def delRoom(self, id: "int") -> bool:

        if Room.query.filter_by(id=id).first() is None:
            return False

        try:
            Room.query.filter_by(id=id).delete()
            self.db.session.commit()
            return True
        except:
            return False

    # Check if there are any meeting scheduled for a given room
    def meetingsScheduledInRoom(self, id: "int") -> bool:
        today = datetime.today()
        room = Room.query.filter_by(id=id).first()

        # No rooms with this id, no meetings scheduled
        if room is None:
            return False

        # Check to see if any future meetings are scheduled
        if Meeting.query.filter(and_(Meeting.start_time > today, Meeting.room_id == room.id)).first():
            return True
        else:
            return False

    # Helper function to build the meeting list to pass to dashboard
    def buildMeetingEvents(self, user: "Client") -> list:
        meetings = []
        if type(user.meetings_participant) is InstrumentedList:
            meetings.extend(user.meetings_participant)
        else:
            meetings.append(user.meetings_participant)

        if type(user.meetings_creator) is InstrumentedList:
            meetings.extend(user.meetings_creator)
        else:
            meetings.append(user.meetings_creator)

        meeting_events = []
        for meeting in meetings:
            meeting_events.append({'id': meeting.id,
                                   'title': meeting.title,
                                   'start': meeting.start_time,
                                   'end': meeting.end_time})

        return meeting_events

    # Helper function to build the meeting list to pass to dashboard
    def buildMeetingListCreator(self, user: "Client") -> list:
        meetings = []

        if type(user.meetings_creator) is InstrumentedList:
            meetings.extend(user.meetings_creator)
        else:
            meetings.append(user.meetings_creator)

        return meetings

    # Helper function to build the meeting list to pass to dashboard
    def buildMeeetingListParticipant(self, user: "Client") -> list:
        meetings = []
        if type(user.meetings_participant) is InstrumentedList:
            meetings.extend(user.meetings_participant)
        else:
            meetings.append(user.meetings_participant)

        return meetings

    # Helper function to create a meeting and add it to the db
    def createMeeting(self, user: "Client", form: "CreateMeetingForm") -> bool:

        try:
            participants = []
            for entry in form.participants.entries:
                participants.append(Client.query.filter_by(email=entry.email.data).first())

            start_time = datetime.combine(form.date.data, form.start_time.data)
            end_time = datetime.combine(form.date.data, form.end_time.data)

            room = form.room.data

            meeting = Meeting(creator_id=user.id, creator=user,
                              title=form.title.data, start_time=start_time, end_time=end_time,
                              description=form.description.data, room_id=room.id,
                              room=room, participants=participants)

            self.db.session.add(meeting)
            self.db.session.commit()

            if room.special:
                utility_controller = UtilityController()
                utility_controller.createBill(user, room)

            return True
        except:
            return False

    # Helper function to edit a meeting and record the changes to the db
    def editMeeting(self, id: "int", form: "CreateMeetingForm") -> bool:

        meeting = Meeting.query.filter_by(id=id).first()

        form = CreateMeetingForm(participants=meeting.participants)
        meeting.title = form.title.data
        meeting.start_time = datetime.combine(form.date.data, form.start_time.data)
        meeting.end_time = datetime.combine(form.date.data, form.end_time.data)
        meeting.description = form.description.data
        print(form.room.data)
        meeting.room = form.room.data

        try:
            self.db.session.commit()
            return True
        except:
            return False

    # Helper function to build edit meeting form
    def buildEditMeetingForm(self, id: "int") -> "CreateMeetingForm":

        meeting = Meeting.query.filter_by(id=id).first()
        if meeting:
            form = CreateMeetingForm(participants=meeting.participants)
            form.title.data = meeting.title
            form.date.data = meeting.start_time.date()
            form.start_time.data = meeting.start_time
            form.end_time.data = meeting.end_time
            form.description.data = meeting.description
            form.room.data = meeting.room

            return form
        else:

            return CreateMeetingForm()

    # Helper function to return meeting dictionary to client side script
    def getMeetingData(self, id: "int") -> dict:
        # find the selected meeting
        meeting = Meeting.query.filter_by(id=id).first()

        # Formatting time to H:M pm/am
        start_formatted = datetime.strptime(f'{meeting.start_time.hour:02d}:{meeting.start_time.minute:02d}',
                                            '%H:%M').strftime('%I:%M %p')
        end_formatted = datetime.strptime(f'{meeting.end_time.hour:02d}:{meeting.end_time.minute:02d}',
                                          '%H:%M').strftime(
            '%I:%M %p')

        # Create dictionary to convert to json
        meeting_json = {'title': meeting.title,
                        'start': start_formatted,
                        'end': end_formatted,
                        'description': meeting.description}

        return meeting_json

    # Helper function to get room cost to client side script
    def getRoomCostData(self, id: "int") -> dict:
        room = Room.query.filter_by(id=id).first()

        if room.special:
            cost = {'cost': '$' + str(room.cost)}
        else:
            cost = {'cost': '-'}

        return cost

    # Helper function to verify current user is meeting creator
    def verifyCreator(self, id: "int", user: "Client") -> bool:
        meeting = Meeting.query.filter_by(id=id).first()
        return meeting.creator == user
