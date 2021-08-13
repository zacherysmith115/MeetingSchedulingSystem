from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user

from mss import app, db
from mss.User.UserModels import Client, User, Admin
from mss.User.UserForms import LoginForm, CreateAccountForm
from mss.User.UserController import UserController

user_controller = UserController()


# Login routing method for both the Admin and Client
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    # Ensure validation of form
    if request.method == 'POST' and form.validate_on_submit():

        # Query the db for email
        user = User.query.filter(User.email == form.email.data).first()

        # Ensure email is in the db and submitted password matches password on record
        if user and user_controller.verifyPassword(form.password.data, user.password):
            login_user(user, remember=False)

            # Route to admin home page
            if isinstance(user, Admin):
                return redirect(url_for('adminDashboard'))

            # Route to client home page
            if isinstance(user, Client):
                return redirect(url_for('dashboard'))

        else:
            flash('Login unsuccessful', 'danger')

    # Credentials failed, resubmit Login page
    return render_template('Login.html', form=form)


# Logout routing method
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
                            password=user_controller.encryptPassword(form.password.data))
            db.session.add(client)
            db.session.commit()
            flash('Account successfully created for ' + form.first_name.data + ' ' + form.last_name.data, 'success')
            return redirect(url_for('login'))
        else:
            flash('Must use a valid company email', 'danger')

    return render_template('CreateAccount.html', form=form)
