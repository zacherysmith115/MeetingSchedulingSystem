from datetime import datetime
from mss.Meeting.MeetingModels import Room

from mss.User.UserModels import Client
from mss.Utility.UtilityModels import Bill, Card
from mss.User.UserForms import PaymentInfoForm

class UtilityController():

    db = None

    def __init__(self) -> None:
        self.db = __import__('mss').db


    # Helper function to build the payment info form when a client accesses the page
    def buildCardInfoForm(self, user: "Client", form: "PaymentInfoForm") -> None:
        card = Card.query.filter_by(client_id = user.id).first()

        # No card attached to account 
        if Card is None:
            return

        form.card_name.data = card.name

        hidden_number = card.number
        hidden_number = '*' * 12 + card.number[len(card.number) - 4:]
        form.card_number.data = hidden_number

        month_str = str(card.exp_date.month)
        if len(month_str) != 2:
            month_str = '0' + month_str

        year_str = str(card.exp_date.year)
        year_str = year_str[2:]

        form.card_exp_date.data = month_str + '/' + year_str


    # Add or update the card information of a user
    def addCard(self, user: "Client", form: "PaymentInfoForm") -> bool:
        card = Card.query.filter_by(client_id = user.id).first()

        exp_date_str = form.card_exp_date.data
        date = datetime(year=int('20' + exp_date_str[3:]), month=int(exp_date_str[0:2]), day=1)

        try:
            # No previous associated card information
            if card is None:
                card = Card(client_id=user.id, name=form.card_name.data,
                            number=form.card_number.data, exp_date=date, ccv=form.card_ccv.data)
                self.db.session.add(card)

            else:
                card.name = form.card_name.data
                card.number = form.card_number.data
                card.exp_date = date
                card.ccv = form.card_ccv.data

            self.db.session.commit()
            return True

        except:
            return False

    # Create bill on room reservation 
    def createBill(self, user: "Client", room: "Room") -> bool:
        bill = Bill(client_id = id, client = user, date = datetime.now(), total = room.cost)

        try:
            self.db.session.add(bill)
            self.db.session.commit()
            return True
        except:
            return False
