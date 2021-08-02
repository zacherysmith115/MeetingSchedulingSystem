from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    check_encrypted_password(password)  # verify against hashed password in db
    submit = SubmitField('Login')

class CreateAccountForm(FlaskForm):
    first_name = StringField('First Name', validators = [DataRequired(), Length(max = 20)])
    last_name = StringField('Last Name', validators = [DataRequired(), Length(max = 20)])
    email = StringField('Email', validators = [DataRequired(), Email(), Length(max = 60)])
    password = PasswordField('Password', validators = [DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    encrypt_password(password)  # encrypt here
    submit = SubmitField('Create Account')
