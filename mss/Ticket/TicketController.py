


from mss.Ticket.TicketForms import NewTicketForm, TicketViewForm
from mss.User.UserModels import User
from mss.Ticket.TicketModels import Ticket



class TicketController():

    db = None

    def __init__(self) -> None:
        self.db = __import__('mss').db

    # Helper function to get the next available ticket number
    def getNewTicketNumber(self) -> int:
        last_ticket = Ticket.query.order_by(Ticket.id.desc()).first()

        return last_ticket.id + 1

    # Helper function to create a new ticket and add it to the db 
    def createTicket(self, user: "User", form: "NewTicketForm") -> bool:
        
        ticket = Ticket(id = form.id.data, content = form.content.data, creator_id = user.id)

        try:
            self.db.session.add(ticket)
            self.db.session.commit()
            return True
        except:
            return False
    
    # Helper function to build the ticket view form 
    def buildTicketViewForm(self, ticket: "Ticket", view: "TicketViewForm") -> None:
        view.id.data = ticket.id
        view.content.data = ticket.content
        view.admin.data = ticket.admin
        view.response.data = ticket.response

    # Helper functiont to build a query for QuerySelectField
    def ticketQueryFactory(self, id: "int"):
        return Ticket.query.filter_by(creator_id = id)

