from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, CreateAccountForm

app = Flask(__name__)
app.config['SECRET_KEY']='653d72d9f6ed01acf0d4'

@app.route("/", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    
    return render_template('Login.html', form=form)

@app.route("/CreateAccount", methods = ['GET', 'POST'])
def createAccount():
    form = CreateAccountForm()
    if form.validate_on_submit():
        flash('Account succesfully created for ' + form.first_name.data + ' ' + form.last_name.data, 'success')
        return redirect(url_for('dashboard'))
   #else:
        #flash('Passwords didn\'t match.', 'danger')
        #return render_template('CreateAccount.html', form=form)

@app.route("/dashboard")
def dashboard():
    return render_template('Dashboard.html')

# Conditional is executed only on "python app.py"
if __name__ == '__main__':
    app.run(debug=True)