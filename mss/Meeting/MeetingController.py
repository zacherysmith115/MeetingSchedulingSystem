from datetime import timedelta, datetime
from sqlalchemy.sql.elements import and_
from sqlalchemy.orm.collections import InstrumentedList

from mss.Meeting.MeetingModels import Meeting, Room
from mss.User.UserModels import Client


class MeetingController():
    db = None

    def __init__(self) -> None:
        self.db = __import__('mss').db

     # Function to provide meetings between a given date and time delta
    def getMeetingsInDelta(self, delta: "timedelta", date: "str") -> list:
        end_time = datetime.strptime(date, '%Y-%m-%d') + delta
        return Meeting.query.filter(and_(Meeting.start_time >= date, Meeting.start_time <= end_time))

    # Function add a room 
    def addRoom(self, id: "int") -> bool:

        # Check room doesnt exist
        if Room.query.filter_by(id=id).first() is None:
            room = Room(id=id, special=False)
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
            Room.query.filter_by(id = id).delete()
            self.db.session.commit()
            return True
        except:
            return False

    
    # Check if there are any meeting scheduled for a given room 
    def meetingsScheduledInRoom(self, id: "int") -> bool:
        today = datetime.today()
        room = Room.query.filter_by(id = id).first()

        # No rooms with this id, no meetings scheudled
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
    
    def buildMeeetingListParticipant(self, user: "Client") -> list:
        meetings = []
        if type(user.meetings_participant) is InstrumentedList:
            meetings.extend(user.meetings_participant)
        else:
            meetings.append(user.meetings_participant)

        return meetings


        
