from flask import render_template, url_for, flash, redirect, request, session
from flask_login import current_user, login_required

from mss import app
from mss.User.UserForms import MeetingSelectForm, EditAccountForm, PaymentInfoForm
from mss.Meeting.MeetingForms import CreateMeetingForm, EditMeetingForm

from mss.User.UserController import UserController
from mss.Meeting.MeetingController import MeetingController
from mss.Ticket.TicketController import TicketController
from mss.Ticket.TicketForms import NewTicketForm, TicketSelectForm, TicketViewForm

from sqlalchemy.orm.collections import InstrumentedList
from mss.User.UserModels import Client

from mss.Utility.UtilityController import UtilityController
from mss.Meeting.MeetingForms import CreateMeetingForm

meeting_controller = MeetingController()
user_controller = UserController()
utility_controller = UtilityController()
ticket_controller = TicketController()


# Client dashboard routing method
@app.route('/User/Dashboard', methods=['GET'])
@login_required
def dashboard():
    # Build meetings list to add to calendar

    meeting_events = meeting_controller.buildMeetingEvents(current_user)
    return render_template('Dashboard.html', events=meeting_events)


# Client my meetings routing method
@app.route('/User/MyMeetings', methods=['GET', 'POST'])
@login_required
def myMeetings():
    form = MeetingSelectForm()

    meetings = meeting_controller.buildMeetingListCreator(current_user)

    if request.method == 'POST' and form.validate_on_submit():
        if form.select.data == '2':
            meetings = meeting_controller.buildMeeetingListParticipant(current_user)

    return render_template('MyMeetings.html', form=form, meetings=meetings)


# Client edit account routing method
@app.route('/User/EditAccount', methods=['GET', 'POST'])
@login_required
def editAccount():
    form = EditAccountForm()

    if request.method == 'POST' and form.validate_on_submit():
        if user_controller.updateAccount(current_user, form):
            flash("Account updated successfully!", 'success')
            return redirect(url_for('editAccount'))
        else:
            flash("Oops something went wrong", "danger")

    if request.method == 'POST' and not form.validate_on_submit():
        user_controller.buildCreateAccountForm(current_user, form)

    user_controller.buildCreateAccountForm(current_user, form)
    return render_template('EditAccount.html', form=form)


# Client add payment info routing method
@app.route('/User/EditAccount/PaymentInfo', methods=['GET', 'POST'])
@login_required
def addPaymentInfo():
    form = PaymentInfoForm()

    utility_controller.buildCardInfoForm(current_user, form)

    # form is validated on submit record to db
    if request.method == 'POST' and form.validate_on_submit():

        if utility_controller.addCard(current_user, form):
            flash('Payment info updated', 'success')

        else:
            flash('Ooops something went wrong! No changes recorded', 'danger')

        return redirect(url_for('addPaymentInfo'))

    return render_template('PaymentInfo.html', form=form)


# Client new ticket routing method
@app.route('/User/TicketCenter/NewTicket', methods=['GET', 'POST'])
@login_required
def newTicket():
    form = NewTicketForm()
    form.id.data = ticket_controller.getNewTicketNumber()

    if request.method == 'POST' and form.validate_on_submit:

        if (ticket_controller.createTicket(current_user, form)):
            flash('Ticket created succesfully!', 'success')
            return redirect(url_for('newTicket'))
        else:
            flash('Oops something went wrong', 'danger')
        

    return render_template('NewTicket.html', form=form)


# Client view old tickets routing method
@app.route('/User/TicketCenter/PastTickets', methods=['GET', 'POST'])
@login_required
def oldTickets():
    form = TicketSelectForm()
    form.ticket_select.query = ticket_controller.ticketQueryFactory(current_user.id)

    if request.method == 'POST' and form.validate_on_submit():
        view = TicketViewForm()
        ticket = form.ticket_select.data
        ticket_controller.buildTicketViewForm(ticket, view)
        return render_template('OldTickets.html', form=form, ticketform=view)

    return render_template('OldTickets.html', form=form)


# Client create meeting routing method
@app.route('/User/Dashboard/CreateMeeting', methods=['GET', 'POST'])
@login_required
def createMeeting():
    form = CreateMeetingForm()

    if request.method == 'POST' and form.validate_on_submit():

        if meeting_controller.createMeeting(current_user, form):
            flash('Meeting added to your calendar!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Oops something went wrong! No changes saved', 'danger')

    return render_template('CreateMeeting.html', form=form, num_participant=len(form.participants.entries))


# Client edit meeting routing method
@app.route('/User/Dashboard/EditMeeting', methods=['GET', 'POST'])
@login_required
def editmeeting():
    # pull meeting id from cookie
    id = session['messages']

    if not meeting_controller.verifyCreator(id, current_user):
        flash('You dont own that meeting', 'danger')
        return redirect(url_for('dashboard'))

    form = EditMeetingForm()

    # Submit changes to commit 
    if request.method == 'POST' and form.validate_edit_on_submit(id):
        if meeting_controller.editMeeting(id, current_user, form):
            flash('Meeting updated!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Oops something went wrong! No changes saved', 'danger')

    # Prepopulate the meeting details
    if request.method == 'GET':
        form = meeting_controller.buildEditMeetingForm(id)

        return render_template('CreateMeeting.html', form=form, num_participant=len(form.participants.entries))

    return render_template('CreateMeeting.html', form=form, num_participant=len(form.participants.entries))
