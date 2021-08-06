from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, jsonify
from mss.forms import *
from mss import app, db
from mss.models import *
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.sql import *


# contains all the routing scripts to navigate the application #

# Login routing method
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # Ensure validation of form
    if form.validate_on_submit():

        # Query the db for email
        user = User.query.filter(User.email == form.email.data).first()

        # Ensure email is in the db and submitted password matches password on record
        if user and user.password == form.password.data:
            login_user(user, remember=False)

            # Route to client home page
            if isinstance(user, Client):
                return redirect(url_for('dashboard'))

            # Route to admin home page
            if isinstance(user, Admin):
                return redirect(url_for('adminDashboard'))
        else:
            flash('Login unsuccessful', 'danger')
    # Credentials failed, resubmit Login page
    return render_template('Login.html', form=form)


@app.route('/Logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# Create account routing method
@app.route("/CreateAccount", methods=['GET', 'POST'])
def createAccount():
    form = CreateAccountForm()
    if form.validate_on_submit():
        if '@pss.com' in form.email.data:
            client = Client(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                            password=form.password.data)
            db.session.add(client)
            db.session.commit()
            flash('Account successfully created for ' + form.first_name.data + ' ' + form.last_name.data, 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Must use a valid company email', 'danger')
    return render_template('CreateAccount.html', form=form)


# Client dashboard routing method
@app.route('/Dashboard', methods=['GET'])
@login_required
def dashboard():
    # Build meetings list to add to calendar
    meetings = []
    if type(current_user.meetings_participant) is InstrumentedList:
        meetings.extend(current_user.meetings_participant)
    else:
        meetings.append(current_user.meetings_participant)

    if type(current_user.meetings_creator) is InstrumentedList:
        meetings.extend(current_user.meetings_creator)
    else:
        meetings.append(current_user.meetings_creator)

    meeting_events = []
    for meeting in meetings:
        meeting_events.append({'id': meeting.id,
                               'title': meeting.title,
                               'start': meeting.start_time,
                               'end': meeting.end_time})

    return render_template('Dashboard.html', events=meeting_events)


# Client my meetings routing method
@app.route('/MyMeetings', methods=['GET', 'POST'])
@login_required
def myMeetings():
    return render_template('MyMeetings.html')


# Client edit account routing method
@app.route('/EditAccount', methods=['GET', 'POST'])
@login_required
def editAccount():
    form = EditAccountForm()

    if not form.validate_on_submit():
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        return render_template('EditAccount.html', form=form)

    if form.validate_on_submit():
        user = User.query.filter(User.id == current_user.id).first()
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.password = form.password.data
        print(user)
        db.session.commit()
        return render_template('EditAccount.html', form=form)

    return render_template('EditAccount.html', form=form)


# Client add payment info routing method
@app.route('/EditAccount/PaymentInfo', methods=['GET', 'POST'])
@login_required
def addPaymentInfo():
    form = PaymentInfoForm()
    card = current_user.card

    # If already has a card populate some of the information
    if not form.validate_on_submit():
        if card is not None:
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

            return render_template('PaymentInfo.html', form=form)

    # form is validated on submit record to db
    if form.validate_on_submit():
        exp_date_str = form.card_exp_date.data
        date = datetime(year=int('20' + exp_date_str[3:]), month=int(exp_date_str[0:2]), day=1)

        # No previous associated card information
        if card is None:
            card = Card(client_id=current_user.id, name=form.card_name.data,
                        number=form.card_number.data, exp_date=date, ccv=form.card_ccv.data)
            db.session.add(card)
        else:
            card = Card.query.filter(Card.client_id == current_user.id).first()
            card.name = form.card_name.data
            card.number = form.card_number.data
            card.exp_date = date
            card.ccv = form.card_ccv.data

        db.session.commit()

        flash('Payment info updated', 'success')
        return render_template('PaymentInfo.html', form=form)

    return render_template('PaymentInfo.html', form=form)


# Client ticket center routing method
@app.route('/TicketCenter', methods=['GET', 'POST'])
@login_required
def ticketCenter():
    return render_template('TicketCenter.html')


# Client ticket center routing method
@app.route('/Help', methods=['GET', 'POST'])
@login_required
def help():
    return render_template('Help.html')


# Admin dashboard routing method
@app.route('/AdminDashboard', methods=['GET'])
@login_required
def adminDashboard():
    return render_template('AdminDashboard.html')


# Admin edit account routing method
@app.route('/AdminEditAccount', methods=['GET', 'POST'])
@login_required
def adminEditAccount():
    form = EditAccountForm()
    return render_template('AdminEditAccount.html', form=form)


# Admin ticket center routing method
@app.route('/AdminTicketCenter', methods=['GET', 'POST'])
@login_required
def adminTicketCenter():
    return render_template('AdminTicketCenter.html')


# Admin display meetings routing method
@app.route('/AdminDisplayMeetings', methods=['GET', 'POST'])
@login_required
def adminDisplayMeetings():
    meetings = ['By Week', 'By Day', 'By Room', 'By Person', 'By Time Slot']
    form = AdminSelectMeeting()
    room = form.select_meeting.data
    if room == 'By Week':
        return render_template('AdminDisplayMeetingsByWeek.html')
    if room == 'By Day':
        return render_template('AdminDisplayMeetingsByDay.html')
    if room == 'By Person':
        return render_template('AdminDisplayMeetingsByPerson.html')
    if room == 'By Room':
        return render_template('AdminDisplayMeetingsByRoom.html')
    if room == 'By Time Slot':
        return render_template('AdminDisplayMeetingsByTime.html')
    else:
        return render_template('AdminDisplayMeetings.html', meetings=meetings, form=form)


# Admin edit admin accounts routing method
@app.route('/AdminEditAdminAccounts', methods=['GET', 'POST'])
@login_required
def adminEditAdminAccounts():
    return render_template('AdminEditAdminAccounts.html')


# Admin edit rooms routing method
@app.route('/AdminEditRooms', methods=['GET', 'POST'])
@login_required
def adminEditRooms():
    delform = DelRoomForm()
    addform = AddRoomForm()

    if delform.validate_on_submit():
        Room.query.filter_by(id=delform.del_room.data).delete()
        db.session.commit()
        flash('Room ' + delform.del_room.data + ' Removed', 'success')
        return redirect(url_for('adminEditRooms'))

    if addform.validate_on_submit():
        print(Room.query.filter_by(id=addform.add_room.data).first())
        # Check if room exists 
        if Room.query.filter_by(id=addform.add_room.data).first() is None:
            room = Room(id=addform.add_room.data, special=False)
            db.session.add(room)
            db.session.commit()
            flash('Room ' + addform.add_room.data + ' Added', 'success')
            return redirect(url_for('adminEditRooms'))

        else:
            flash('Room ' + addform.add_room.data + ' already exists! No changes made.', 'danger')
            return redirect(url_for('adminEditRooms'))

    return render_template('AdminEditRooms.html', delform=delform, addform=addform, rooms=Room.query.all())


# Admin update bill routing method
@app.route('/AdminUpdateUserBill', methods=['GET', 'POST'])
@login_required
def adminUpdateUserBill():
    form = UpdateUserBill()

    if form.validate_on_submit():
        total = Bill(id=form.total.data, special=False)
        db.session.add(total)
        db.session.commit()
        flash('Bill updated')
        return redirect(url_for('adminUpdateUserBill'))

    # else:
    #    flash('Error please try again')
    #    return redirect(url_for('adminUpdateUserBill'))

    return render_template('AdminUpdateUserBill.html', form=form, clients=Client.query.all(), user=User.query.all(),
                           bill=Bill.query.all())


@app.route('/getmeetingdata/<index_no>', methods=['GET'])
@login_required
def getMeetingData(index_no):
    # find the selected meeting
    meeting = Meeting.query.filter_by(id=index_no).first()

    # Formatting time to H:M pm/am
    start_formatted = datetime.strptime(f'{meeting.start_time.hour:02d}:{meeting.start_time.minute:02d}',
                                        '%H:%M').strftime('%I:%M %p')
    end_formatted = datetime.strptime(f'{meeting.end_time.hour:02d}:{meeting.end_time.minute:02d}', '%H:%M').strftime(
        '%I:%M %p')

    # Create json "like" object
    meeting_json = {'title': meeting.title,
                    'start': start_formatted,
                    'end': end_formatted,
                    'description': meeting.description}

    return jsonify(meeting_json)


@app.route('/dashboard/createMeeting', methods=['GET', 'POST'])
@login_required
def createMeeting():
    form = CreateMeetingForm()
    if request.method == 'GET':
        times = []
        for i in range(7, 17):
            for j in range(0, 60, 15):
                times.append(datetime.time(i, j).strftime("%I:%M %p"))

        form.start_time.choices = [(i, times[i]) for i in range(0, len(times))]
        form.end_time.choices = [(i, times[i]) for i in range(0, len(times))]

        return render_template('CreateMeeting.html', form=form)

    if request.method == 'POST':
        return redirect(url_for('dashboard'))

    return render_template('AdminUpdateUserBill.html', form=form, clients=Client.query.all(), user=User.query.all(),
                           bill=Bill.query.all())
