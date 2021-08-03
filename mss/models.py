from mss import db, login_manager
from flask_login import UserMixin

# contains all the database models User, Client, Admin, Card, Bill
# refrence = https://docs.sqlalchemy.org/en/13/_modules/examples/inheritance/joined.html, 
#            https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html


# table to map many to many relationship
participation_table = db.Table('association', db.metadata, 
                    db.Column('meeting', db.ForeignKey('meeting.id'), primary_key=True),
                    db.Column('participant', db.ForeignKey('client.id'), primary_key=True))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# User model class
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    type = db.Column(db.String(60), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'User',
        'polymorphic_on': type
    }

    def __repr__(self) -> str:
        return f"User: {self.first_name} {self.last_name}"


# Cleint model class: one to one relationship with card and one to many relationship with bill
class Client(User):
    __tablename__ = 'client'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    # one to one relationship with card
    card = db.relationship('Card', back_populates='client', uselist=False)

    # one to many relationship with bill
    bills = db.relationship('Bill', back_populates='client')

    # one to many relationship with meeting
    meetings_creator = db.relationship('Meeting', back_populates='creator', uselist=False)
    
    # many to many relationship with meeting
    meetings_participant = db.relationship('Meeting', secondary=participation_table, back_populates='participants') 

    # one to many relationship with ticket
    tickets = db.relationship('Ticket', back_populates='creator', uselist=False)

    __mapper_args__ = {
        'polymorphic_identity':'client'
    }

    def __repr__(self) -> str:
        return f"Client: {self.first_name} {self.last_name}"


# Admin model class
class Admin(User):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    # one to many relationship with ticket
    tickets = db.relationship('Ticket', back_populates='admin', uselist=False)

    __mapper_args__ = {
        'polymorphic_identity':'admin'
    }

    def __repr__(self) -> str:
        return f"Admin: {self.first_name} {self.last_name}"


# Payment info model class
class Card(db.Model):
    __tablename__ = 'card'

    id = db.Column(db.Integer, primary_key=True)

    # one to one relationship with client
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship('Client', back_populates='card')

    number = db.Column(db.String(16), nullable = False)
    name = db.Column(db.String(60), nullable = False)
    exp_date = db.Column(db.DateTime, nullable = False)
    ccv = db.Column(db.String(3), nullable = False)


# Billing model class
class Bill(db.Model):
    __tablename__ = 'bill'

    id = db.Column(db.Integer, primary_key=True)

    # many to one relationship with client
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship('Client', back_populates='bills')

    date = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f'Bill: {self.id}, {self.date}, {self.total}'


# Meeting model class
class Meeting(db.Model):
    __tablename__ = 'meeting'

    id = db.Column(db.Integer, primary_key=True)

    # one to many relationship with Client
    creator_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False) 
    creator = db.relationship('Client', back_populates='meetings_creator')

    # many to many relationship with meeting
    participants = db.relationship('Client', secondary=participation_table, back_populates='meetings_participant') 

    # many to one relationship with room
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    room = db.relationship('Room', back_populates='meetings')


    title = db.Column(db.String(240), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self) -> str:
        return f'Bill: {self.title}\n\tStart: {self.start_time}\n\tEnd: {self.total}\n\tRoom:{self.room_id}'

# Room model class
class Room(db.Model):
    __tablename__ = 'room'

    id = db.Column(db.Integer, primary_key=True)
    special = db.Column(db.Boolean, default=False)
    cost = db.Column(db.Integer, default=50)

    # one to many relationship with meeting
    meetings = db.relationship('Meeting', back_populates='room')

    def __repr__(self) -> str:
        return f'Room {self.id}'

# Ticket model class
class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)

    # many to one relationship with Client 
    creator_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    creator = db.relationship('Client', back_populates='tickets')

    # many to one relationship with Admin
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)
    admin = db.relationship('Admin', back_populates='tickets')

    def __repr__(self) -> str:
        return f'Ticket {self.id}'