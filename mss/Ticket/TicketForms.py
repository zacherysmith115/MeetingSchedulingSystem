from flask_wtf.form import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from mss.Ticket.TicketModels import Ticket


class NewTicketForm(FlaskForm):

    id = IntegerField('Ticket Number', render_kw={'readonly': True}, validators=[DataRequired()])
    content = TextAreaField('Complaint', validators=[DataRequired()])

    submit = SubmitField('Create Ticket')

class TicketSelectForm(FlaskForm):
    user_id = None
    ticket_select = QuerySelectField(query_factory = lambda: Ticket.query, allow_blank=False, validators=[DataRequired()])

    submit = SubmitField('View')

class TicketViewForm(FlaskForm):
    id = IntegerField('Ticket Number', render_kw={'readonly': True})
    content = TextAreaField('Complaint', render_kw={'readonly': True})
    admin = StringField('Admin', render_kw={'readonly': True})
    response = TextAreaField('Response', render_kw={'readonly': True})

class TicketResponseForm(FlaskForm):
    id = IntegerField('Ticket Number', render_kw={'readonly': True})
    content = TextAreaField('Complaint', render_kw={'readonly': True})
    admin = StringField('Admin', render_kw={'readonly': True})
    response = TextAreaField('Response', validators=[DataRequired()])
    
    submit = SubmitField('Respond')
    

