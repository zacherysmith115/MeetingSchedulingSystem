from datetime import date
from mss.Utility.UtilityForms import UpdateBillForm
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
        if not card:
            return

        form.card_name.data = card.name

        hidden_number = card.number
        hidden_number = '*' * 12 + card.number[len(card.number) - 4:]
        form.card_number.data = hidden_number
        form.card_exp_date.data = card.exp_date


    # Add or update the card information of a user
    def addCard(self, user: "Client", form: "PaymentInfoForm") -> bool:
        card = Card.query.filter_by(client_id = user.id).first()

        try:
            # No previous associated card information
            if card is None:
                card = Card(client_id=user.id, name=form.card_name.data,
                            number=form.card_number.data, exp_date=form.card_exp_date.data, ccv=form.card_ccv.data)
                self.db.session.add(card)

            else:
                card.name = form.card_name.data
                card.number = form.card_number.data
                card.exp_date = form.card_exp_date.data
                card.ccv = form.card_ccv.data

            self.db.session.commit()
            return True

        except Exception as e:
            print(e)
            return False

    # Create bill on room reservation 
    def createBill(self, user: "Client", room: "Room") -> bool:
        bill = Bill(client_id = id, client = user, date = date.today(), total = room.cost)

        try:
            self.db.session.add(bill)
            self.db.session.commit()
            return True
        except:
            return False

    # Helper function to build update user bill form 
    def buildUpdateBillForm(self, client: "Client", form: "UpdateBillForm") -> None:
        
        total = 0
        for bill in client.bills:
            total = total + bill.total 

        form.current_total.data = '$' + str(total)
        form.client.data = client
        form.client_id.data = client.id

    # Helper function to update a client's current bill
    def updateBill(self, form: "UpdateBillForm") -> bool:
        

        current_total = int(form.current_total.data.replace('$', ''))
        new_total = int(form.new_total.data.replace('$', ''))
        delta = new_total - current_total
        
        

        client = Client.query.filter_by(id = int(form.client_id.data)).first()
        bill = Bill(client_id = client.id, client = client, date = date.today(), total = delta)
        
        self.db.session.add(bill)
        self.db.session.commit()
        return True
