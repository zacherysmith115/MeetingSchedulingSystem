from mss.Ticket.TicketController import TicketController
from mss.Ticket.TicketForms import TicketResponseForm, TicketSelectForm
from mss.Meeting.MeetingController import MeetingController
from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_required
from sqlalchemy.sql.expression import and_
from datetime import datetime, timedelta

from mss import app, db

from mss.Utility.UtilityModels import Bill
from mss.Meeting.MeetingModels import Meeting

from mss.Utility.UtilityForms import *
from mss.Meeting.MeetingForms import AddRoomForm, DelRoomForm
from mss.User.UserForms import EditAccountForm

from mss.User.UserController import UserController
from mss.Meeting.MeetingController import MeetingController

from mss.User.UserModels import Admin
from mss.User.UserForms import AdminEditAdminAccountsForm

user_controller = UserController()
meeting_controller = MeetingController()
ticket_controller = TicketController()


# Admin dashboard routing method -> reroute to display meetings
@app.route('/Admin/Dashboard', methods=['GET'])
@login_required
def adminDashboard():
    return redirect(url_for('adminDisplayMeetings'))


# Admin edit account routing method
@app.route('/Admin/EditAccount', methods=['GET', 'POST'])
@login_required
def adminEditAccount():
    form = EditAccountForm()

    if request.method == 'GET':
        user_controller.buildCreateAccountForm(current_user, form)
        return render_template('AdminEditAccount.html', form=form)

    if request.method == 'POST' and form.validate_on_submit():

        # db updated succesfully
        if user_controller.updateAccount(current_user, form):
            flash('Account Updated!', 'success')
            redirect(url_for('adminDashboard'))

        else:
            flash('Oops! Something went wrong, no changes were saved', 'danger')
            return render_template('AdminEditAccount.html', form=form)

    return render_template('AdminEditAccount.html', form=form)


# Admin ticket center routing method
@app.route('/Admin/TicketCenter', methods=['GET', 'POST'])
@login_required
def adminTicketCenter():
    form = TicketSelectForm()
    form.ticket_select.query = ticket_controller.adminTicketQueryFactory()

    view = TicketResponseForm()

    if request.method == 'POST' and form.validate_on_submit():
        ticket = form.ticket_select.data

        ticket_controller.buildResponseViewform(current_user, ticket, view)
        return render_template('AdminTicketCenter.html', form=form, ticketform=view)

    if request.method == 'POST' and view.validate_on_submit():
        form = TicketSelectForm()
        form.ticket_select.query = ticket_controller.adminTicketQueryFactory()

        if ticket_controller.addResponse(current_user, view):

            flash('Reponse recorded!', 'success')
            return render_template('AdminTicketCenter.html', form=form)
        else:
            flash('Oops! Something went wrong, no changes recorded', 'danger')
            return render_template('AdminTicketCenter.html', form=form)

    return render_template('AdminTicketCenter.html', form=form)


# Admin display meetings routing method
@app.route('/Admin/DisplayMeetings', methods=['GET', 'POST'])
@login_required
def adminDisplayMeetings():
    form = AdminSelectMeeting()

    if request.method == 'GET':
        return render_template('AdminDisplayMeetings.html', form=form)

    if request.method == 'POST' and form.validate_on_submit():
        selection = form.select_meeting.data

        if selection == '1':
            return redirect(url_for('adminDisplayMeetingsByWeek'))
        if selection == '2':
            return redirect(url_for('adminDisplayMeetingsByDay'))
        if selection == '3':
            return redirect(url_for('adminDisplayMeetingsByPerson'))
        if selection == '4':
            return redirect(url_for('adminDisplayMeetingsByRoom'))
        if selection == '5':
            return redirect(url_for('adminDisplayMeetingsByTime'))

    return render_template('AdminDisplayMeetings.html', form=form)


# Admin Display Meetings By Week
@app.route('/Admin/DisplayMeetings/ByWeek', methods=['GET', 'POST'])
@login_required
def adminDisplayMeetingsByWeek():
    form = AdminSelectMeetingByDay()
    form.dt.label.text = 'Select Start of Week:'

    if request.method == 'POST' and form.validate_on_submit():
        meetings = meeting_controller.getMeetingsInDelta(timedelta(days=7), form.dt.data.strftime('%Y-%m-%d'))

        return render_template('AdminDisplayMeetingsByWeek.html', meetings=meetings, form=form)

    return render_template('AdminDisplayMeetingsByWeek.html', form=form)


# Admin Display Meetings By Day
@app.route('/Admin/DisplayMeetings/ByDay', methods=['GET', 'POST'])
@login_required
def adminDisplayMeetingsByDay():
    form = AdminSelectMeetingByDay()

    if request.method == 'POST' and form.validate_on_submit():
        meetings = meeting_controller.getMeetingsInDelta(timedelta(days=1), form.dt.data.strftime('%Y-%m-%d'))

        return render_template('AdminDisplayMeetingsByDay.html', meetings=meetings, form=form)

    return render_template('AdminDisplayMeetingsByDay.html', form=form)


# Admin Display Meetings By Person
@app.route('/Admin/DisplayMeetings/ByPerson', methods=['GET', 'POST'])
@login_required
def adminDisplayMeetingsByPerson():
    form = AdminSelectMeetingByPerson()

    if request.method == 'POST' and form.validate_on_submit():
        meetings = Meeting.query.filter(Meeting.creator == form.select_person.data)
        return render_template('AdminDisplayMeetingsByPerson.html', form=form, meetings=meetings)

    return render_template('AdminDisplayMeetingsByPerson.html', form=form)


# Admin Display Meetings By Room
@app.route('/Admin/DisplayMeetings/ByRoom', methods=['GET', 'POST'])
@login_required
def adminDisplayMeetingsByRoom():
    form = AdminSelectMeetingByRoom()

    if request.method == 'POST' and form.validate_on_submit():
        meetings = Meeting.query.filter(Meeting.room == form.select_room.data)
        return render_template('AdminDisplayMeetingsByRoom.html', form=form, meetings=meetings)

    return render_template('AdminDisplayMeetingsByRoom.html', form=form)


# Admin Display Meetings By Time
@app.route('/Admin/DisplayMeetings/ByTime', methods=['GET', 'POST'])
@login_required
def adminDisplayMeetingsByTime():
    form = AdminSelectMeetingByTime()

    if request.method == 'POST' and form.validate_on_submit():
        start = datetime.combine(form.dt_start_date.data,
                                 form.dt_start_time.data).strftime('%Y-%m-%d %H:%M:00')

        end = datetime.combine(form.dt_end_date.data,
                               form.dt_end_time.data).strftime('%Y-%m-%d %H:%M:00')

        meetings = Meeting.query.filter(and_(Meeting.start_time >= start, Meeting.start_time <= end))

        return render_template('AdminDisplayMeetingsByTime.html', meetings=meetings, form=form)

    return render_template('AdminDisplayMeetingsByTime.html', form=form)


# Admin edit rooms routing method
@app.route('/Admin/EditRooms', methods=['GET', 'POST'])
@login_required
def adminEditRooms():
    delform = DelRoomForm()
    addform = AddRoomForm()

    # Delete room request
    if request.method == 'POST' and delform.validate_on_submit():

        # Meetings still scheduled 
        if meeting_controller.meetingsScheduledInRoom(delform.del_room.data):
            flash('Room ' + delform.del_room.data + ' still has scheduled meetings!', 'danger')
            return redirect(url_for('adminEditRooms'))

        if meeting_controller.delRoom(delform.del_room.data):
            flash('Room ' + delform.del_room.data + ' removed!', 'success')
        else:
            flash('Oops! Something went wrong. No changes saved.', 'danger')

        return redirect(url_for('adminEditRooms'))

    # Add room request
    if request.method == 'POST' and addform.validate_on_submit():

        if meeting_controller.addRoom(addform.add_room.data):
            flash('Room ' + addform.add_room.data + ' added!', 'success')
        else:
            flash('Oops! Something went wrong. No changes saved.', 'danger')

        return redirect(url_for('adminEditRooms'))

    return render_template('AdminEditRooms.html', delform=delform, addform=addform, rooms=Room.query.all())


# Admin update bill routing method
@app.route('/Admin/UpdateUserBill', methods=['GET', 'POST'])
@login_required
def adminUpdateUserBill():
    form = UpdateUserBill()

    if request.method == 'POST' and form.validate_on_submit():
        bill = Bill(client_id=form.client_id.data, date=form.date.data, total=form.total.data)
        db.session.add(bill)
        db.session.commit()
        flash('Bill updated', 'success')

        return redirect(url_for('adminUpdateUserBill'))

    return render_template('AdminUpdateUserBill.html', form=form)


# Admin create admin account routing method
@app.route("/Admin/EditAdminAccounts", methods=['GET', 'POST'])
@login_required
def editAdminAccounts():
    form = AdminEditAdminAccountsForm()

    if form.validate_on_submit():
        if '@pss.com' in form.email.data:
            admin = Admin(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                          password=user_controller.encryptPassword(form.password.data))
            db.session.add(admin)
            db.session.commit()
            flash('Admin Account successfully created for ' + form.first_name.data + ' ' + form.last_name.data)
            return redirect(url_for('adminDashboard'))
        else:
            flash('Must use a valid company email', 'danger')
    return render_template('AdminEditAdminAccounts.html', title='Create New Admin Account', form=form)
