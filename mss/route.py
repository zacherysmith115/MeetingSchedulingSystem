from datetime import datetime, time, date, timedelta
from flask import render_template, url_for, flash, redirect, request, jsonify, Flask
from flask_wtf import Form
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
    form = AdminSelectMeeting()
    form.select_meeting.choices = ['By Week', 'By Day', 'By Room', 'By Person', 'By Time Slot']
    room = form.select_meeting.data
    if room == "By Week":
        return redirect(url_for('adminDisplayMeetingsByWeek'))
    if room == 'By Day':
        return redirect(url_for('adminDisplayMeetingsByDay'))
    if room == 'By Person':
        return redirect(url_for('adminDisplayMeetingsByPerson'))
    if room == 'By Room':
        return redirect(url_for('adminDisplayMeetingsByRoom'))
    if room == 'By Time Slot':
        return redirect(url_for('adminDisplayMeetingsByTime'))
    else:
        return render_template('AdminDisplayMeetings.html', form=form)


# Admin Display Meetings By Week
@app.route('/AdminDisplayMeetingsByWeek', methods=['GET', 'POST'])
@login_required
def adminDisplayMeetingsByWeek():
    form = AdminSelectMeetingByWeek()
    delta = datetime.timedelta(days=7)
    meetings = Meeting.query.filter(None)
    if form.validate_on_submit():
        selected_week = form.dt.data.strftime('%Y-%m-%d')
        end_time = datetime.datetime.strptime(selected_week, '%Y-%m-%d') + delta
        meetings = Meeting.query.filter(and_(Meeting.start_time >= selected_week, Meeting.start_time <= end_time))

    return render_template('AdminDisplayMeetingsByWeek.html', meetings=meetings, form=form)


# Admin Display Meetings By Day
@app.route('/AdminDisplayMeetingsByDay', methods=['GET', 'POST'])
@login_required
def adminDisplayMeetingsByDay():
    form = AdminSelectMeetingByDay()
    delta = datetime.timedelta(days=1)
    meetings = Meeting.query.filter(None)
    if form.validate_on_submit():
        selected_week = form.dt.data.strftime('%Y-%m-%d')
        end_time = datetime.datetime.strptime(selected_week, '%Y-%m-%d') + delta
        meetings = Meeting.query.filter(and_(Meeting.start_time >= selected_week, Meeting.start_time <= end_time))

    return render_template('AdminDisplayMeetingsByDay.html', meetings=meetings, form=form)


# Admin Display Meetings By Person
@app.route('/AdminDisplayMeetingsByPerson', methods=['GET', 'POST'])
@login_required
def adminDisplayMeetingsByPerson():
    form = AdminSelectMeetingByPerson()
    meetings = Meeting.query.filter(None)
    if form.validate_on_submit():
        meetings = Meeting.query.filter(Meeting.creator == form.select_person.data)
    return render_template('AdminDisplayMeetingsByPerson.html', form=form, meetings=meetings)


# Admin Display Meetings By Room
@app.route('/AdminDisplayMeetingsByRoom', methods=['GET', 'POST'])
@login_required
def adminDisplayMeetingsByRoom():
    form = AdminSelectMeetingByRoom()
    meetings = Meeting.query.filter(None)
    if form.validate_on_submit():
        meetings = Meeting.query.filter(Meeting.room == form.select_room.data)
    return render_template('AdminDisplayMeetingsByRoom.html', form=form, meetings=meetings)


# Admin Display Meetings By Time
@app.route('/AdminDisplayMeetingsByTime', methods=['GET', 'POST'])
@login_required
def adminDisplayMeetingsByTime():
    form = AdminSelectMeetingByTime()
    meetings = Meeting.query.filter(None)
    if form.validate_on_submit():
        start = datetime.datetime.combine(form.dt_start_date.data,
                                          form.dt_start_time.data).strftime('%Y-%m-%d %H:%M:00')
        end = datetime.datetime.combine(form.dt_end_date.data,
                                        form.dt_end_time.data).strftime('%Y-%m-%d %H:%M:00')
        meetings = Meeting.query.filter(and_(Meeting.start_time >= start, Meeting.start_time <= end))
    return render_template('AdminDisplayMeetingsByTime.html', meetings=meetings, form=form)


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
    
@app.route('/getroomcost/<room_no>', methods=['GET'])
@login_required
def getRoomCost(room_no):
    room = Room.query.filter_by(id = room_no).first()
    
    if room.special:
        cost = {'cost': '$' + str(room.cost)}
    else:
        cost = {'cost': '-'}

    return jsonify(cost)


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
        
        participants=[]
        for entry in form.participants.entries:
           
            participants.append(Client.query.filter_by(email=entry.email.data).first())


        start_time = datetime.combine(form.date.data, datetime.strptime(form.start_time.data, "%I:%M %p").time())
        end_time = datetime.combine(form.date.data, datetime.strptime(form.end_time.data, "%I:%M %p").time())

        room = Room.query.filter_by(id=form.room.data).first()
        
        meeting = Meeting(creator_id=current_user.id, creator=current_user,
                        title=form.title.data, start_time=start_time, end_time=end_time,
                        description=form.description.data, room_id=room.id,
                        room=room, participants=participants)
        
        print(type(meeting.creator_id))

        db.session.add(meeting)
        db.session.commit()

        flash('Meeting added to your calendar!', 'success')
        return redirect(url_for('dashboard'))

        
    return render_template('CreateMeeting.html', form=form)
    
