from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Login')

class CreateAccountForm(FlaskForm):
    first_name = StringField('First Name', validators = [DataRequired(), Length(max = 20)])
    last_name = StringField('Last Name', validators = [DataRequired(), Length(max = 20)])
    email = StringField('Email', validators = [DataRequired(), Email(), Length(max = 60)])
    password = PasswordField('Password', validators = [DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Create Account')


    //test
