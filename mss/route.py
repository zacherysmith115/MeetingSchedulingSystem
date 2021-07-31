from flask import render_template, url_for, flash, redirect
from mss.forms import EditAccountForm, LoginForm, CreateAccountForm
from mss import app, db
from mss.usermodels import User, Client

 # contains all the routing script to navigate the application #

@app.route("/", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data)[0]
        if(user.password == form.password.data):
            return redirect(url_for('dashboard'))

    return render_template('Login.html', form=form)

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

@app.route("/Dashboard", methods = ['GET'])
def dashboard():
    return render_template('Dashboard.html')

@app.route("/EditAccount", methods = ['GET', 'POST'])
def editAccount():
    form = EditAccountForm()
    return render_template('EditAccount.html', form = form)