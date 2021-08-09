from mss import db

# Ticket model class
class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=True)

    # many to one relationship with Client 
    creator_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    creator = db.relationship('mss.User.UserModels.Client', back_populates='tickets')

    # many to one relationship with Admin
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)
    admin = db.relationship('mss.User.UserModels.Admin', back_populates='tickets')

    def __repr__(self) -> str:
        return f'Ticket {self.id}'
