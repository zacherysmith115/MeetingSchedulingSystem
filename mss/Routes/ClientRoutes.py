from flask import render_template, url_for, flash, redirect, request,  session
from flask_login import current_user, login_required

from mss import app
from mss.User.UserForms import MeetingSelectForm, EditAccountForm, PaymentInfoForm
from mss.Meeting.MeetingForms import CreateMeetingForm

from mss.Utility.UtilityController import UtilityController
from mss.User.UserController import UserController
from mss.Meeting.MeetingController import MeetingController

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
    if request.method == 'POST' and form.validate_on_submit():
        
        if utility_controller.addCard(current_user, form):
            flash('Payment info updated', 'success')
            
        else:
            flash('Ooops something went wrong! No changes recorded', 'danger')
        
        redirect(url_for('addPaymentInfo'))

    return render_template('PaymentInfo.html', form=form)



# Client ticket center routing method
@app.route('/User/TicketCenter', methods=['GET', 'POST'])
@login_required
def ticketCenter():
    return render_template('TicketCenter.html')



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

    return render_template('CreateMeeting.html', form=form)



# Cleint edit meeting routing method
@app.route('/User/Dashboard/EditMeeting', methods=['GET', 'POST'])
@login_required
def editmeeting():

    # pull meeting id from cookie
    id = session['messages']

    form = CreateMeetingForm()

    # Submit changes to commit 
    if request.method == 'POST' and form.validate_on_submit():
        if meeting_controller.editMeeting(id, form):
            flash('Meeting updated!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Oops something went wrong! No changes saved', 'danger')

    # Prepopulate the meeting details
    if request.method == 'GET':
        form = meeting_controller.buildEditMeetingForm(id)
        return render_template('CreateMeeting.html', form=form)

    return render_template('CreateMeeting.html', form=form)