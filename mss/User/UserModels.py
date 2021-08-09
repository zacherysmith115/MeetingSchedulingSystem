from mss import db, login_manager
from flask_login import UserMixin
from mss.Meeting.MeetingModels import Meeting
from mss.Ticket.TicketModels import Ticket
from mss.Utility.UtilityModels import participation_table, Bill

# Decorator to get current user during request
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# User model class: Client and Admin are modeled as subclasses to User
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    type = db.Column(db.String(60), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def __repr__(self) -> str:
        return f"User: {self.first_name} {self.last_name}"


# Client model class: one to one relationship with card and one to many relationship with bill
class Client(User):
    __tablename__ = 'client'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    # one to many relationship with bill
    bills = db.relationship('Bill', back_populates='client')

    # one to many relationship with meeting
    meetings_creator = db.relationship('Meeting', back_populates='creator')

    # many to many relationship with meeting
    meetings_participant = db.relationship('Meeting', secondary=participation_table, back_populates='participants')

    # one to many relationship with ticket
    tickets = db.relationship('Ticket', back_populates='creator')

    __mapper_args__ = {
        'polymorphic_identity': 'client'
    }

    def __repr__(self) -> str:
        return f"Client: {self.first_name} {self.last_name}"


# Admin model class
class Admin(User):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    # one to many relationship with ticket
    tickets = db.relationship('Ticket', back_populates='admin')

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    def __repr__(self) -> str:
        return f"Admin: {self.first_name} {self.last_name}"