from mss import db

# table to map many to many relationship
participation_table = db.Table('association', db.metadata,
                               db.Column('meeting', db.ForeignKey('meeting.id'), primary_key=True),
                               db.Column('participant', db.ForeignKey('client.id'), primary_key=True))

# Payment info model class
class Card(db.Model):
    __tablename__ = 'card'

    id = db.Column(db.Integer, primary_key=True)

    # one to one relationship with client
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship('mss.User.UserModels.Client', backref=db.backref('card'))

    number = db.Column(db.String(16), nullable=False)
    name = db.Column(db.String(60), nullable=False)
    exp_date = db.Column(db.DateTime, nullable=False)
    ccv = db.Column(db.String(3), nullable=False)

    def __repr__(self) -> str:
        return f'{self.name}: *************{self.number[12:]}'

# Billing model class
class Bill(db.Model):
    __tablename__ = 'bill'

    id = db.Column(db.Integer, primary_key=True)

    # many to one relationship with client
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship('mss.User.UserModels.Client', back_populates='bills')

    date = db.Column(db.Date, nullable=False)
    total = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f'Bill: {self.id}, {self.date}, {self.total}'