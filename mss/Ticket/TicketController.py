from mss.Ticket.TicketForms import NewTicketForm, TicketResponseForm, TicketViewForm
from mss.User.UserModels import Admin, User
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


    # Factory method to build query based on user id
    def ticketQueryFactory(self, id: "int"):
        return Ticket.query.filter_by(creator_id = id)


    # Facory method to build query for unresponded tickets
    def adminTicketQueryFactory(self):
        return Ticket.query.filter(Ticket.response == None)


    # Helper function to populate admin response view
    def buildResponseViewform(self, user: "Admin",  ticket: "Ticket", view: "TicketResponseForm") -> None:
        view.id.data = ticket.id
        view.content.data = ticket.content
        view.admin.data = user
    

    # Helper function to attach an admin response to a ticket 
    def addResponse(self, user: "Admin", view: "TicketResponseForm") -> bool:
        ticket = Ticket.query.filter_by(id = view.id.data).first()

        ticket.response = view.response.data
        ticket.admin_id = user.id
        ticket.admin = user
        
        try:
            self.db.session.commit()
            return True            
        except:
            return False