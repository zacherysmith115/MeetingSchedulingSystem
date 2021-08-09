from sqlalchemy import util
from mss.Utility.UtilityController import UtilityController
from re import L
from mss.User.UserController import UserController
from mss.Meeting.MeetingController import MeetingController
from mss.Meeting.MeetingModels import Meeting, Room
from mss.Meeting.MeetingForms import CreateMeetingForm
from flask import render_template, url_for, flash, redirect, request,  session
from flask_login import current_user, login_required
from datetime import datetime, time

from mss import app, db
from mss.User.UserModels import Client, User
from mss.Utility.UtilityModels import Card
from mss.User.UserForms import MeetingSelectForm
from mss.User.UserForms import EditAccountForm, PaymentInfoForm

meeting_controller = MeetingController()
user_controller = UserController()
utility_controller = UtilityController()

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
            print('ran')
            meetings = meeting_controller.buildMeeetingListParticipant(current_user)

    return render_template('MyMeetings.html', form=form, meetings=meetings)



# Client edit account routing method
@app.route('/User/EditAccount', methods=['GET', 'POST'])
@login_required
def editAccount():
    form = EditAccountForm()

    if request.method == 'POST' and form.validate_on_submit():
        user_controller.updateAccount(current_user, form)
        flash("Account updated succesfully!", 'success')
        redirect(url_for('editAccount'))

    if request.method == 'POST' and not form.validate_on_submit():
        user_controller.buildCreateAccountForm(current_user, form)
    
    user_controller.buildCreateAccountForm(current_user, form)
    return render_template('EditAccount.html', form=form)



# Client add payment info routing method
@app.route('/User/EditAccount/PaymentInfo', methods=['GET', 'POST'])
@login_required
def addPaymentInfo():
    form = PaymentInfoForm()
    card = current_user.card[0]
    
    utility_controller.buildCardInfoForm(current_user, form) 
    
    # form is validated on submit record to db
    if form.validate_on_submit():
        
        if utility_controller.addCard(current_user, form):
            flash('Payment info updated', 'success')
        else:
            flash('Ooops something went wrong! No changes recorded', 'danger')
        
        redirect(url_for('addPaymentInfo'))


    return render_template('PaymentInfo.html', form=form)

# Client ticket center routing method
@app.route('/TicketCenter', methods=['GET', 'POST'])
@login_required
def ticketCenter():
    return render_template('TicketCenter.html')


@app.route('/dashboard/createMeeting', methods=['GET', 'POST'])
@login_required
def createMeeting():
    form = CreateMeetingForm()

    # build selectable times for the form
    times = []
    for i in range(7, 17):
        for j in range(0, 60, 15):
            times.append(time(i, j).strftime('%I:%M %p'))

    form.start_time.choices = [times[i] for i in range(0, len(times))]
    form.end_time.choices = [times[i] for i in range(0, len(times))]

    # build selectable rooms for the form
    rooms = []
    for room in Room.query.all():
        rooms.append(room.id)

    form.room.choices = rooms

    if request.method == 'POST' and form.validate_on_submit():

        participants = []
        for entry in form.participants.entries:
            participants.append(Client.query.filter_by(email=entry.email.data).first())

        start_time = datetime.combine(form.date.data, datetime.strptime(form.start_time.data, "%I:%M %p").time())
        end_time = datetime.combine(form.date.data, datetime.strptime(form.end_time.data, "%I:%M %p").time())

        room = Room.query.filter_by(id=form.room.data).first()

        meeting = Meeting(creator_id=current_user.id, creator=current_user,
                        title=form.title.data, start_time=start_time, end_time=end_time,
                        description=form.description.data, room_id=room.id,
                        room=room, participants=participants)

        db.session.add(meeting)
        db.session.commit()

        flash('Meeting added to your calendar!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('CreateMeeting.html', form=form)



@app.route('/dashboard/editmeeting', methods=['GET', 'POST'])
@login_required
def editmeeting():

    # pull meeting id from cookie
    id = session['messages']
    meeting = Meeting.query.filter_by(id=id).first()

    form = CreateMeetingForm(participants = meeting.participants)
    times = []
    for i in range(7, 17):
        for j in range(0, 60, 15):
            times.append(time(i, j).strftime('%I:%M %p'))

    form.start_time.choices = [times[i] for i in range(0, len(times))]
    form.end_time.choices = [times[i] for i in range(0, len(times))]

    rooms = []
    for room in Room.query.all():
        rooms.append(room.id)

    form.room.choices = rooms

    if request.method == 'GET':
        form.title.data = meeting.title
        form.date.data = meeting.start_time.date()
        # add preselected time?
        form.description.data = meeting.description
        return render_template('CreateMeeting.html', form=form)


    return render_template('CreateMeeting.html', form=form)