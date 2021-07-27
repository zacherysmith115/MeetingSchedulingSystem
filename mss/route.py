from flask import render_template, url_for, flash, redirect
from mss.forms import LoginForm, CreateAccountForm
from mss import app

 # contains all the routing script to navigate the application #

@app.route("/", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('dashboard'))
    return render_template('Login.html', form=form)

@app.route("/CreateAccount", methods = ['GET', 'POST'])
def createAccount():
    form = CreateAccountForm()
    if form.validate_on_submit():
        flash('Account succesfully created for ' + form.first_name.data + ' ' + form.last_name.data, 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('CreateAccount.html', form = form)

@app.route("/dashboard")
def dashboard():
    return render_template('Dashboard.html')