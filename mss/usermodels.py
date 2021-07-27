from mss import db


# contains all the database models

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on': str
    }

    def __repr__(self):
        return f"User: {self.first_name} {self.last_name}"

# no idea if this will work ref = https://docs.sqlalchemy.org/en/14/orm/inheritance.html
class Client(User):
    __tablename__ = 'client'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    card = db.relationship('card', backref='client', lazy=True)
    bills = db.relationship('bill', backref='client', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity':'client'
    }

    def __repr__(self):
        return f"Client: {self.first_name} {self.last_name}"

class Admin(User):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'admin'
    }

    def __repr__(self):
        return f"Admin: {self.first_name} {self.last_name}"


class Card(db.Model):
    __tablename = 'card'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Long, nullable = False)
    name = db.Column(db.String(60), nullable = False)
    expDate = db.Column(db.DateTime, nullable = False)
    ccv = db.Column()

class Bill(db.Model):
    __tablename__ = 'bill'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

