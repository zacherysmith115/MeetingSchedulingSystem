from mss import db

# contains all the database models
# refrence = https://docs.sqlalchemy.org/en/13/_modules/examples/inheritance/joined.html

class User(db.Model):
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



class Client(User):
    __tablename__ = 'client'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    #card = db.relationship('Card', back_populates='client', cascade='all, delete-orphan')
    #bills = db.relationship('Bill', back_populates='client', cascade='all, delete-orphan')

    __mapper_args__ = {
        'polymorphic_identity':'client'
    }

    def __repr__(self) -> str:
        return f"Client: {self.first_name} {self.last_name}"



class Admin(User):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'admin'
    }

    def __repr__(self) -> str:
        return f"Admin: {self.first_name} {self.last_name}"



# class Card(db.Model):
#     __tablename__ = 'card'

#     id = db.Column(db.Integer, primary_key=True)
#     client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

#     number = db.Column(db.String(16), nullable = False)
#     name = db.Column(db.String(60), nullable = False)
#     expDate = db.Column(db.DateTime, nullable = False)
#     ccv = db.Column(db.String(3), nullable = False)



# class Bill(db.Model):
#     __tablename__ = 'bill'

#     id = db.Column(db.Integer, primary_key=True)
#     client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

#     date = db.Column(db.DateTime, nullable=False)
#     total = db.Column(db.Integer, nullable=False)

#     def __repr__(self) -> str:
#         return f'Bill: {self.id}, {self.date}, {self.total}'

