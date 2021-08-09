from flask_wtf.form import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from mss.Ticket.TicketModels import Ticket


def ticketQuery(id: "int"):
    return Ticket.query.filter_by(creator_id = id)

class NewTicketForm(FlaskForm):

    id = IntegerField('Ticket Number', render_kw={'readonly': True}, validators=[DataRequired()])
    content = TextAreaField('Complaint', validators=[DataRequired()])

    submit = SubmitField('Create Ticket')

class TicketSelectForm(FlaskForm):
    user_id = None
    ticket_select = QuerySelectField(query_factory = ticketQuery, allow_blank=False)

    submit = SubmitField('View')

class TicketViewForm(FlaskForm):
    id = IntegerField('Ticket Number', render_kw={'readonly': True})
    content = TextAreaField('Complaint', render_kw={'readonly': True})
    admin = StringField('Admin', render_kw={'readonly': True})
    response = TextAreaField('Response', render_kw={'readonly': True})


