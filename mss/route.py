from flask import render_template, url_for, flash, redirect
from mss.forms import EditAccountForm, LoginForm, CreateAccountForm, PaymentInfoForm
from mss import app, db
from mss.models import User, Client, Admin

 # contains all the routing scripts to navigate the application #


# Login routing method
@app.route('/', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    # Ensure validation of form
    if form.validate_on_submit():

        # Query the db for email
        user = db.session.query(User).filter(User.email == form.email.data).first()

        # Ensure email is in the db and submited password matches password on record
        if(user and user.password == form.password.data):

            # Route to client home page
            if(isinstance(user, Client)):
                return redirect(url_for('dashboard'))

            # Route to admin home page
            if(isinstance(user, Admin)):
                return redirect(url_for('adminDashboard'))
        
    # Credentials failed, resumbit Login page
    return render_template('Login.html', form=form)



# Create account routing method
@app.route("/CreateAccount", methods = ['GET', 'POST'])
def createAccount():
    form = CreateAccountForm()
    if form.validate_on_submit():
        if '@pss.com' in form.email.data:
            client = Client(first_name = form.first_name.data, last_name = form.last_name.data, email = form.email.data, password = form.password.data)
            db.session.add(client)
            db.session.commit()
            flash('Account succesfully created for ' + form.first_name.data + ' ' + form.last_name.data, 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Must use a valid compnay email', 'danger')
    return render_template('CreateAccount.html', form = form)



# Client dashboard routing method
@app.route('/Dashboard', methods = ['GET'])
def dashboard():
    return render_template('Dashboard.html')

# Client my meetings routing method
@app.route('/MyMeetings', methods = ['GET', 'POST'])
def myMeetings():
    return render_template('MyMeetings.html')

# Client edit account routing method
@app.route('/EditAccount', methods = ['GET', 'POST'])
def editAccount():
    form = EditAccountForm()
    return render_template('EditAccount.html', form = form)

# Client add payment info routing method
@app.route('/EditAccount/PaymentInfo', methods = ['GET', 'POST'])
def addPaymentInfo():
    form = PaymentInfoForm()
    return render_template('PaymentInfo.html', form = form)

# Client ticket center routing method
@app.route('/TicketCenter', methods =['GET', 'POST'])
def ticketCenter():
    return render_template('TicketCenter.html')

# Client ticket center routing method
@app.route('/Help', methods =['GET', 'POST'])
def help():
    return render_template('Help.html')


# Admin dashboard routing method
@app.route('/AdminDashboard', methods = ['GET'])
def adminDashboard():
    return render_template('AdminDashboard.html')

# Admin edit account routing method
@app.route('/AdminEditAccount', methods = ['GET', 'POST'])
def adminEditAccount():
    form = EditAccountForm()
    return render_template('AdminEditAccount.html', form = form)

# Admin ticket center routing method
@app.route('/AdminTicketCenter', methods = ['GET', 'POST'])
def adminTicketCenter():
    return render_template('AdminTicketCenter.html')

# Admin display meetings routing method
@app.route('/AdminDisplayMeeetings', methods =['GET', 'POST'])
def adminDisplayMeetings():
    return render_template('AdminDisplayMeetings.html')

# Admin edit admin accounts routing method
@app.route('/AdminEditAdminAccounts', methods =['GET', 'POST'])
def adminEditAdminAccounts():
    return render_template('AdminEditAdminAccounts.html')

# Admin edit rooms routing method
@app.route('/AdminEditRooms', methods =['GET', 'POST'])
def adminEditRooms():
    return render_template('AdminEditRooms.html')

# Admin edit rooms routing method
@app.route('/AdminUpdateUserBill', methods =['GET', 'POST'])
def adminUpdateUserBill():
    return render_template('AdminUpdateUserBill.html')