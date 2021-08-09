from mss import db
from mss.Utility.UtilityModels import participation_table

# Meeting model class
class Meeting(db.Model):
    __tablename__ = 'meeting'

    id = db.Column(db.Integer, primary_key=True)

    # one to many relationship with Client
    creator_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    creator = db.relationship('mss.User.UserModels.Client', back_populates='meetings_creator')

    # many to many relationship with meeting
    participants = db.relationship('mss.User.UserModels.Client', secondary=participation_table, back_populates='meetings_participant')

    # many to one relationship with room
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    room = db.relationship('Room', back_populates='meetings')

    title = db.Column(db.String(240), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        return f'Meeting: {self.title}\n\tStart: {self.start_time}\n\tEnd: {self.end_time}\n\tRoom:{self.room_id}'


# Room model class
class Room(db.Model):
    __tablename__ = 'room'

    id = db.Column(db.Integer, primary_key=True)
    special = db.Column(db.Boolean, default=False)
    cost = db.Column(db.Integer, default=None)

    # one to many relationship with meeting
    meetings = db.relationship('Meeting', back_populates='room')

    def __repr__(self) -> str:
        return f'Room {self.id}'